from django.conf import settings
from django.db import models


class Task(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pendente', 'Pendente'
        DONE = 'concluida', 'Concluída'
        CANCELED = 'cancelada', 'Cancelada'

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks',
    )
    lead = models.ForeignKey(
        'leads.Lead',
        on_delete=models.SET_NULL,
        related_name='tasks',
        null=True,
        blank=True,
    )
    contact = models.ForeignKey(
        'contacts.Contact',
        on_delete=models.SET_NULL,
        related_name='tasks',
        null=True,
        blank=True,
    )
    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descrição', blank=True)
    due_date = models.DateField('Data de vencimento')
    status = models.CharField(
        'Status',
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        ordering = ['due_date', 'status']
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        from django.utils import timezone

        if self.status != self.Status.PENDING:
            return False
        return self.due_date < timezone.localdate()
