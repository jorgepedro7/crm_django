import csv
from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView

from accounts.models import Account
from contacts.models import Contact
from leads.models import Lead
from tasks.models import Task


class HomePageView(TemplateView):
    template_name = 'home.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    login_url = 'users:login'
    monthly_goal = 10
    month_span = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        today = timezone.localdate()
        accounts_total = Account.objects.filter(owner=user).count()
        contacts_total = Contact.objects.filter(owner=user).count()
        leads_total = Lead.objects.filter(owner=user).count()
        tasks_qs = Task.objects.filter(owner=user)
        tasks_total = tasks_qs.count()
        pending_total = tasks_qs.filter(status=Task.Status.PENDING).count()
        overdue_total = tasks_qs.filter(
            status=Task.Status.PENDING, due_date__lt=today
        ).count()
        overdue_tasks = tasks_qs.filter(
            status=Task.Status.PENDING, due_date__lt=today
        ).order_by('due_date')[:3]
        upcoming_tasks = tasks_qs.filter(
            status=Task.Status.PENDING, due_date__gte=today
        ).order_by('due_date')[:3]
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
            percent = round((step_count / leads_total) * 100) if leads_total else 0
            pipeline_steps.append(
                {
                    'name': status_labels.get(status_value, status_value.title()),
                    'count': step_count,
                    'color': status_palette.get(status_value, 'bg-slate-500'),
                    'percent': percent,
                }
            )
        converted_total = status_map.get(Lead.Status.CONVERTED, 0)
        qualified_total = status_map.get(Lead.Status.QUALIFIED, 0)
        active_leads_total = max(
            leads_total - status_map.get(Lead.Status.LOST, 0), 0
        )
        conversion_rate = (
            round((converted_total / leads_total) * 100, 1) if leads_total else 0
        )
        recent_conversions = (
            Lead.objects.filter(owner=user, status=Lead.Status.CONVERTED)
            .select_related('account')
            .order_by('-updated_at')[:10]
        )
        monthly_stats = self._build_monthly_stats(user, today)
        monthly_chart = self._build_monthly_chart(monthly_stats)
        context.update(
            {
                'accounts_total': accounts_total,
                'contacts_total': contacts_total,
                'leads_total': leads_total,
                'tasks_total': tasks_total,
                'tasks_pending_total': pending_total,
                'overdue_total': overdue_total,
                'overdue_tasks': overdue_tasks,
                'upcoming_tasks': upcoming_tasks,
                'recent_conversions': recent_conversions,
                'pipeline_steps': pipeline_steps,
                'monthly_stats': monthly_stats,
                'monthly_goal': self.monthly_goal,
                'monthly_chart': monthly_chart,
                'headline_metrics': [
                    {
                        'label': 'Leads ativos',
                        'value': active_leads_total,
                        'trend': f'{qualified_total} qualificados',
                    },
                    {
                        'label': 'Taxa de conversão',
                        'value': f'{conversion_rate}%',
                        'trend': f'{converted_total} convertidos',
                    },
                    {
                        'label': 'Tarefas pendentes',
                        'value': pending_total,
                        'trend': f'{overdue_total} vencidas',
                    },
                    {
                        'label': 'Contas ativas',
                        'value': accounts_total,
                        'trend': f'{contacts_total} contatos vinculados',
                    },
                ],
                'quick_links': [
                    {'label': 'Leads', 'href': reverse_lazy('leads:list')},
                    {'label': 'Contas', 'href': reverse_lazy('accounts:list')},
                    {'label': 'Contatos', 'href': reverse_lazy('contacts:list')},
                    {'label': 'Tarefas', 'href': reverse_lazy('tasks:list')},
                    {'label': 'Relatórios', 'href': reverse_lazy('reports')},
                ],
            }
        )
        return context

    def _shift_month(self, base_date, offset):
        month = base_date.month + offset
        year = base_date.year + (month - 1) // 12
        month = (month - 1) % 12 + 1
        return base_date.replace(year=year, month=month, day=1)

    def _build_monthly_stats(self, user, today):
        base_month = today.replace(day=1)
        month_keys = [
            self._shift_month(base_month, -i)
            for i in range(self.month_span - 1, -1, -1)
        ]
        earliest_month = month_keys[0]
        monthly_rows = (
            Lead.objects.filter(owner=user, created_at__date__gte=earliest_month)
            .annotate(period=TruncMonth('created_at'))
            .values('period')
            .annotate(
                total=Count('id'),
                converted=Count('id', filter=Q(status=Lead.Status.CONVERTED)),
            )
        )
        monthly_map = {
            row['period'].date(): {
                'total': row['total'],
                'converted': row['converted'],
            }
            for row in monthly_rows
        }
        stats = []
        for month in month_keys:
            row = monthly_map.get(month, {'total': 0, 'converted': 0})
            stats.append(
                {
                    'label': month.strftime('%b/%y'),
                    'total': row['total'],
                    'converted': row['converted'],
                    'goal': self.monthly_goal,
                    'goal_delta': row['converted'] - self.monthly_goal,
                }
            )
        return stats

    def _build_monthly_chart(self, stats):
        max_value = max(
            [max(item['total'], item['converted']) for item in stats] or [1]
        )
        step = 100 / max(len(stats) - 1, 1)
        leads_points = []
        converted_points = []
        for idx, item in enumerate(stats):
            x = idx * step
            leads_y = 100 - ((item['total'] / max_value) * 100 if max_value else 0)
            converted_y = 100 - (
                (item['converted'] / max_value) * 100 if max_value else 0
            )
            leads_points.append(f'{x:.2f},{leads_y:.2f}')
            converted_points.append(f'{x:.2f},{converted_y:.2f}')
        return {
            'width': 100,
            'height': 100,
            'leads_points': ' '.join(leads_points),
            'converted_points': ' '.join(converted_points),
            'max_value': max_value,
        }


class ReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/report.html'
    login_url = 'users:login'

    def _parse_date(self, value):
        if not value:
            return None
        try:
            return datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            return None

    def _get_date_filters(self):
        today = timezone.localdate()
        default_start = today - timedelta(days=30)
        start_param = self.request.GET.get('data_inicio')
        end_param = self.request.GET.get('data_fim')
        start_date = self._parse_date(start_param) or default_start
        end_date = self._parse_date(end_param) or today
        if start_date > end_date:
            start_date, end_date = end_date, start_date
        return start_date, end_date

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        start_date, end_date = self._get_date_filters()
        base_qs = Lead.objects.filter(owner=user)
        if start_date:
            base_qs = base_qs.filter(created_at__date__gte=start_date)
        if end_date:
            base_qs = base_qs.filter(created_at__date__lte=end_date)

        total_leads = base_qs.count()
        converted_total = base_qs.filter(status=Lead.Status.CONVERTED).count()
        conversion_rate = (
            round((converted_total / total_leads) * 100, 1) if total_leads else 0
        )

        source_rows = (
            base_qs.values('source')
            .annotate(
                total=Count('id'),
                converted=Count('id', filter=Q(status=Lead.Status.CONVERTED)),
            )
            .order_by('-total')
        )
        source_summary = []
        for row in source_rows:
            total = row['total']
            converted = row['converted']
            source_value = row['source']
            label = dict(Lead.Source.choices).get(source_value, 'Não informado')
            source_summary.append(
                {
                    'source': source_value,
                    'label': label,
                    'total': total,
                    'converted': converted,
                    'conversion_rate': round((converted / total) * 100, 1)
                    if total
                    else 0,
                }
            )

        status_rows = (
            base_qs.values('status')
            .annotate(total=Count('id'))
            .order_by('-total')
        )
        status_summary = []
        for row in status_rows:
            status_value = row['status']
            status_summary.append(
                {
                    'status': status_value,
                    'label': dict(Lead.Status.choices).get(status_value, status_value),
                    'total': row['total'],
                    'percent': round((row['total'] / total_leads) * 100, 1)
                    if total_leads
                    else 0,
                }
            )

        context.update(
            {
                'filter_start': start_date,
                'filter_end': end_date,
                'total_leads': total_leads,
                'converted_total': converted_total,
                'conversion_rate': conversion_rate,
                'source_summary': source_summary,
                'status_summary': status_summary,
            }
        )
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.GET.get('export') == 'csv':
            return self._export_csv(context)
        return super().render_to_response(context, **response_kwargs)

    def _export_csv(self, context):
        filename = (
            f"relatorio_{context['filter_start']:%Y-%m-%d}_{context['filter_end']:%Y-%m-%d}.csv"
        )
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        writer = csv.writer(response)
        writer.writerow(['Origem', 'Leads', 'Convertidos', 'Taxa (%)'])
        for row in context['source_summary']:
            writer.writerow(
                [row['label'], row['total'], row['converted'], row['conversion_rate']]
            )
        return response
