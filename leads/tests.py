import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.models import Account
from .models import Lead, LeadStatus

User = get_user_model()


class LeadTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='lead-owner@example.com',
            password='test1234',
        )
        self.account = Account.objects.create(owner=self.user, name='Zeta Ltda')
        self.client.force_login(self.user)

    def test_lead_conversion_creates_relations(self):
        lead = Lead.objects.create(
            owner=self.user,
            name='Teste Lead',
            email='lead@example.com',
            status=Lead.Status.NEW,
        )
        response = self.client.post(reverse('leads:convert', args=[lead.pk]))
        self.assertRedirects(response, reverse('leads:list'))
        lead.refresh_from_db()
        self.assertEqual(lead.status, Lead.Status.CONVERTED)
        self.assertIsNotNone(lead.account)
        self.assertIsNotNone(lead.contact)

    def test_lead_list_search(self):
        Lead.objects.create(
            owner=self.user,
            name='Alfa Company',
            email='alfa@example.com',
        )
        response = self.client.get(reverse('leads:list'), {'q': 'Alfa'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alfa Company')


class KanbanTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='kanban@example.com',
            password='test1234',
        )
        self.client.force_login(self.user)
        self.status_new = LeadStatus.objects.get(key=Lead.Status.NEW)
        self.status_qualified = LeadStatus.objects.get(key=Lead.Status.QUALIFIED)
        self.lead_a = Lead.objects.create(
            owner=self.user,
            name='Kanban Lead A',
            email='kanban-a@example.com',
            status=Lead.Status.NEW,
        )
        self.lead_b = Lead.objects.create(
            owner=self.user,
            name='Kanban Lead B',
            email='kanban-b@example.com',
            status=Lead.Status.NEW,
        )

    def test_kanban_view_renders(self):
        response = self.client.get(reverse('leads:kanban'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Kanban de Leads')

    def test_update_lead_position_endpoint(self):
        payload = {
            'lead_id': self.lead_b.id,
            'status': Lead.Status.NEW,
            'position': 0,
        }
        response = self.client.post(
            reverse('leads:kanban_update'),
            data=json.dumps(payload),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.lead_b.refresh_from_db()
        self.assertEqual(self.lead_b.position, 0)
