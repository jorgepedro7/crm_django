from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.models import Account
from .models import Contact

User = get_user_model()


class ContactTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='contact-owner@example.com',
            password='test1234',
        )
        self.account = Account.objects.create(owner=self.user, name='Gamma SA')
        self.client.force_login(self.user)

    def test_create_contact(self):
        contact = Contact.objects.create(
            owner=self.user,
            account=self.account,
            name='Maria',
            email='maria@example.com',
        )
        self.assertEqual(str(contact), 'Maria (Gamma SA)')

    def test_list_view(self):
        Contact.objects.create(
            owner=self.user,
            account=self.account,
            name='João',
            email='joao@example.com',
        )
        response = self.client.get(reverse('contacts:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'João')
