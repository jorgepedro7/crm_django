from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from leads.models import Lead
from .models import Task

User = get_user_model()


class TaskTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='tasks@example.com',
            password='test1234',
        )
        self.lead = Lead.objects.create(
            owner=self.user,
            name='Lead Task',
            email='lead-task@example.com',
        )

    def test_is_overdue_property(self):
        task = Task.objects.create(
            owner=self.user,
            lead=self.lead,
            title='Follow-up',
            due_date=timezone.localdate() - timedelta(days=1),
        )
        self.assertTrue(task.is_overdue)

    def test_task_list_requires_login(self):
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 302)
        self.client.force_login(self.user)
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 200)
