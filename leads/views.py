from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.views.generic.detail import SingleObjectMixin

from accounts.models import Account
from contacts.models import Contact
from .forms import LeadForm
from .models import Lead
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


class LeadCreateView(LeadFormMixin, CreateView):
    template_name = 'leads/lead_form.html'


class LeadUpdateView(LeadFormMixin, UpdateView):
    template_name = 'leads/lead_form.html'


class LeadDeleteView(LeadBaseMixin, DeleteView):
    template_name = 'leads/lead_confirm_delete.html'
    success_url = reverse_lazy('leads:list')


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
