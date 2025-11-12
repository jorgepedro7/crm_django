from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from accounts.models import Account
from contacts.models import Contact


class HomePageView(TemplateView):
    template_name = 'home.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    login_url = 'users:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        accounts_total = Account.objects.filter(owner=self.request.user).count()
        contacts_total = Contact.objects.filter(owner=self.request.user).count()
        context.update(
            {
                'accounts_total': accounts_total,
                'contacts_total': contacts_total,
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
                'pipeline_steps': [
                    {
                        'name': 'Novos',
                        'count': 12,
                        'color': 'bg-cyan-400',
                        'percent': 80,
                    },
                    {
                        'name': 'Qualificados',
                        'count': 9,
                        'color': 'bg-indigo-400',
                        'percent': 65,
                    },
                    {
                        'name': 'Propostas',
                        'count': 6,
                        'color': 'bg-purple-400',
                        'percent': 45,
                    },
                    {
                        'name': 'Ganhamos',
                        'count': 3,
                        'color': 'bg-emerald-400',
                        'percent': 30,
                    },
                ],
                'quick_links': [
                    {'label': 'Contas', 'href': '#accounts'},
                    {'label': 'Contatos', 'href': reverse_lazy('contacts:list')},
                    {'label': 'Leads', 'href': '#leads'},
                    {'label': 'Tarefas', 'href': '#tasks'},
                    {'label': 'Relatórios', 'href': '#reports'},
                ],
            }
        )
        return context
