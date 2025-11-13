from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from leads.models import Lead

User = get_user_model()


class ReportsViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='qa@example.com',
            password='test1234',
        )
        self.client.force_login(self.user)

    def _create_lead(
        self,
        email,
        status=Lead.Status.NEW,
        source=Lead.Source.INBOUND,
        days_ago=0,
    ):
        lead = Lead.objects.create(
            owner=self.user,
            name=email.split('@')[0],
            email=email,
            phone='11999990000',
            source=source,
            status=status,
        )
        if days_ago:
            created = timezone.now() - timedelta(days=days_ago)
            Lead.objects.filter(pk=lead.pk).update(
                created_at=created,
                updated_at=created,
            )
        return lead

    def test_reports_context_with_aggregations(self):
        self._create_lead(
            'a@example.com',
            status=Lead.Status.CONVERTED,
            source=Lead.Source.OUTBOUND,
        )
        self._create_lead(
            'b@example.com',
            status=Lead.Status.LOST,
            source=Lead.Source.OUTBOUND,
        )

        response = self.client.get(reverse('reports'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_leads'], 2)
        self.assertEqual(response.context['converted_total'], 1)
        self.assertEqual(response.context['conversion_rate'], 50.0)
        self.assertTrue(response.context['source_summary'])

    def test_reports_csv_export(self):
        self._create_lead(
            'export@example.com',
            status=Lead.Status.CONVERTED,
            source=Lead.Source.EVENT,
        )
        params = {
            'data_inicio': timezone.localdate().replace(day=1).isoformat(),
            'data_fim': timezone.localdate().isoformat(),
            'export': 'csv',
        }
        response = self.client.get(reverse('reports'), params)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        content = response.content.decode()
        self.assertIn('Origem', content)
        self.assertIn('Convertidos', content)


class DashboardMonthlyStatsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='owner@example.com',
            password='test1234',
        )
        self.client.force_login(self.user)

    def _create_lead(self, email, status, days_ago):
        lead = Lead.objects.create(
            owner=self.user,
            name=email.split('@')[0],
            email=email,
            phone='11999990000',
            source=Lead.Source.INBOUND,
            status=status,
        )
        created = timezone.now() - timedelta(days=days_ago)
        Lead.objects.filter(pk=lead.pk).update(
            created_at=created,
            updated_at=created,
        )
        return lead

    def test_dashboard_monthly_stats_present(self):
        self._create_lead('jane@example.com', Lead.Status.CONVERTED, 30)
        self._create_lead('john@example.com', Lead.Status.NEW, 5)

        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
        monthly_stats = response.context['monthly_stats']
        self.assertTrue(monthly_stats)
        chart = response.context['monthly_chart']
        self.assertTrue(chart['leads_points'])
        self.assertTrue(chart['converted_points'])
