import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView
from django.views.generic.detail import SingleObjectMixin

from accounts.models import Account
from contacts.models import Contact
from .forms import LeadForm
from .models import Lead, LeadStatus
from .signals import lead_converted


class LeadBaseMixin(LoginRequiredMixin):
    model = Lead
    login_url = 'users:login'

    def get_queryset(self):
        return (
            Lead.objects.filter(owner=self.request.user)
            .select_related('account', 'contact')
            .order_by('-created_at')
        )


class LeadListView(LeadBaseMixin, ListView):
    template_name = 'leads/lead_list.html'
    context_object_name = 'leads'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        status = self.request.GET.get('status')
        source = self.request.GET.get('source')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
                | Q(email__icontains=query)
                | Q(phone__icontains=query)
                | Q(account__name__icontains=query)
            )
        if status:
            queryset = queryset.filter(status=status)
        if source:
            queryset = queryset.filter(source=source)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'selected_status': self.request.GET.get('status', ''),
                'selected_source': self.request.GET.get('source', ''),
                'status_choices': Lead.Status.choices,
                'source_choices': Lead.Source.choices,
            }
        )
        return context


class LeadFormMixin(LeadBaseMixin):
    form_class = LeadForm
    success_url = reverse_lazy('leads:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class LeadCreateView(SuccessMessageMixin, LeadFormMixin, CreateView):
    template_name = 'leads/lead_form.html'
    success_message = 'Lead cadastrado com sucesso.'


class LeadUpdateView(SuccessMessageMixin, LeadFormMixin, UpdateView):
    template_name = 'leads/lead_form.html'
    success_message = 'Lead atualizado com sucesso.'


class LeadDeleteView(LeadBaseMixin, DeleteView):
    template_name = 'leads/lead_confirm_delete.html'
    success_url = reverse_lazy('leads:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Lead excluído com sucesso.')
        return super().delete(request, *args, **kwargs)


class LeadConvertView(LeadBaseMixin, SingleObjectMixin, View):
    success_url = reverse_lazy('leads:list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        lead = self.object
        if lead.status == Lead.Status.CONVERTED:
            messages.info(request, 'Este lead já foi convertido anteriormente.')
            return redirect(self.success_url)

        account = lead.account
        if not account:
            account, _ = Account.objects.get_or_create(
                owner=request.user,
                name=lead.name,
                defaults={'industry': '', 'city': '', 'website': ''},
            )

        contact = lead.contact
        if not contact:
            contact, _ = Contact.objects.get_or_create(
                owner=request.user,
                email=lead.email,
                defaults={
                    'account': account,
                    'name': lead.name,
                    'phone': lead.phone,
                    'position': 'Contato principal',
                },
            )
        if contact.account != account:
            contact.account = account
            contact.save(update_fields=['account'])

        lead.account = account
        lead.contact = contact
        lead.save(update_fields=['account', 'contact', 'updated_at'])
        lead_converted.send(sender=Lead, lead=lead, user=request.user)
        messages.success(request, 'Lead convertido com sucesso em conta e contato.')
        return redirect(self.success_url)


class KanbanView(LoginRequiredMixin, TemplateView):
    template_name = 'leads/kanban.html'
    login_url = 'users:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        statuses = LeadStatus.objects.order_by('order')
        leads = (
            Lead.objects.filter(owner=self.request.user)
            .select_related('account', 'contact')
            .order_by('position', 'created_at')
        )
        leads_by_status = {status.key: [] for status in statuses}
        for lead in leads:
            leads_by_status.setdefault(lead.status, []).append(lead)
        columns = [
            {'status': status, 'leads': leads_by_status.get(status.key, [])}
            for status in statuses
        ]
        context['kanban_columns'] = columns
        return context


class UpdateLeadPositionView(LoginRequiredMixin, View):
    login_url = 'users:login'

    def post(self, request, *args, **kwargs):
        try:
            payload = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Payload inválido.'}, status=400)

        lead_id = payload.get('lead_id')
        new_status = payload.get('status')
        new_position = payload.get('position')

        if None in (lead_id, new_status, new_position):
            return JsonResponse({'success': False, 'error': 'Dados incompletos.'}, status=400)

        if not LeadStatus.objects.filter(key=new_status).exists():
            return JsonResponse({'success': False, 'error': 'Status inválido.'}, status=400)

        try:
            lead = Lead.objects.get(pk=lead_id, owner=request.user)
        except Lead.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Lead não encontrado.'}, status=404)

        try:
            new_position = int(new_position)
            if new_position < 0:
                raise ValueError
        except (ValueError, TypeError):
            return JsonResponse({'success': False, 'error': 'Posição inválida.'}, status=400)

        with transaction.atomic():
            old_status = lead.status
            updated_at = timezone.now()
            self._insert_in_new_column(request.user, lead, new_status, new_position, updated_at)
            if old_status != new_status:
                self._resequence_column(request.user, old_status)

        return JsonResponse({'success': True})

    def _insert_in_new_column(self, user, lead, new_status, new_position, updated_at):
        column_qs = (
            Lead.objects.filter(owner=user, status=new_status)
            .exclude(pk=lead.pk)
            .order_by('position', 'updated_at')
        )
        leads = list(column_qs)
        new_position = min(new_position, len(leads))
        leads.insert(new_position, lead)
        for idx, item in enumerate(leads):
            if item.pk == lead.pk:
                Lead.objects.filter(pk=lead.pk).update(
                    status=new_status,
                    position=idx,
                    updated_at=updated_at,
                )
            else:
                if item.position != idx:
                    Lead.objects.filter(pk=item.pk).update(position=idx)

    def _resequence_column(self, user, status):
        qs = (
            Lead.objects.filter(owner=user, status=status)
            .order_by('position', 'updated_at')
        )
        for idx, item in enumerate(qs):
            if item.position != idx:
                Lead.objects.filter(pk=item.pk).update(position=idx)
