from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Account

User = get_user_model()


class AccountTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='owner@example.com',
            password='test1234',
        )
        self.client.force_login(self.user)

    def test_str_representation(self):
        account = Account.objects.create(owner=self.user, name='ACME')
        self.assertEqual(str(account), 'ACME')

    def test_list_view_returns_accounts(self):
        Account.objects.create(owner=self.user, name='Beta Inc')
        response = self.client.get(reverse('accounts:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Beta Inc')
