from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Profile


class ProfileSignalTests(TestCase):
    def test_profile_is_created_on_user_creation(self):
        user = get_user_model().objects.create_user(
            email='profile@example.com',
            password='test1234',
        )
        self.assertTrue(Profile.objects.filter(user=user).exists())
