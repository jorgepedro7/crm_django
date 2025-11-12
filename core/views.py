from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from accounts.models import Account
from contacts.models import Contact
from leads.models import Lead


class HomePageView(TemplateView):
    template_name = 'home.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    login_url = 'users:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        accounts_total = Account.objects.filter(owner=user).count()
        contacts_total = Contact.objects.filter(owner=user).count()
        leads_total = Lead.objects.filter(owner=user).count()
        status_totals = (
            Lead.objects.filter(owner=user)
            .values('status')
            .annotate(total=Count('id'))
        )
        status_map = {item['status']: item['total'] for item in status_totals}
        status_palette = {
            Lead.Status.NEW: 'bg-cyan-400',
            Lead.Status.QUALIFIED: 'bg-indigo-400',
            Lead.Status.CONVERTED: 'bg-emerald-400',
            Lead.Status.LOST: 'bg-rose-400',
        }
        status_labels = {
            Lead.Status.NEW: 'Novos',
            Lead.Status.QUALIFIED: 'Qualificados',
            Lead.Status.CONVERTED: 'Convertidos',
            Lead.Status.LOST: 'Perdidos',
        }
        pipeline_steps = []
        for status_value in Lead.Status.values:
            step_count = status_map.get(status_value, 0)
            percent = int((step_count / leads_total) * 100) if leads_total else 0
            pipeline_steps.append(
                {
                    'name': status_labels.get(status_value, status_value.title()),
                    'count': step_count,
                    'color': status_palette.get(status_value, 'bg-slate-500'),
                    'percent': percent,
                }
            )
        recent_conversions = (
            Lead.objects.filter(owner=user, status=Lead.Status.CONVERTED)
            .select_related('account')
            .order_by('-updated_at')[:10]
        )
        context.update(
            {
                'accounts_total': accounts_total,
                'contacts_total': contacts_total,
                'leads_total': leads_total,
                'recent_conversions': recent_conversions,
                'pipeline_steps': pipeline_steps,
                'headline_metrics': [
                    {
                        'label': 'Leads ativos',
                        'value': 18,
                        'trend': '+12% vs semana anterior',
                    },
                    {
                        'label': 'Taxa de conversão',
                        'value': '32%',
                        'trend': '+4 pts',
                    },
                    {
                        'label': 'Follow-ups do dia',
                        'value': 7,
                        'trend': '3 atrasados',
                    },
                ],
                'quick_links': [
                    {'label': 'Leads', 'href': reverse_lazy('leads:list')},
                    {'label': 'Contas', 'href': reverse_lazy('accounts:list')},
                    {'label': 'Contatos', 'href': reverse_lazy('contacts:list')},
                    {'label': 'Tarefas', 'href': '#tasks'},
                    {'label': 'Relatórios', 'href': '#reports'},
                ],
            }
        )
        return context
