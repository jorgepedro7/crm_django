from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class LoginViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='login@example.com',
            password='test1234',
        )

    def test_login_template_renders(self):
        response = self.client.get(reverse('users:login'))
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_flow(self):
        response = self.client.post(
            reverse('users:login'),
            {'username': 'login@example.com', 'password': 'test1234'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
