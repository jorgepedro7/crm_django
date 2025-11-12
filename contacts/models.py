from django.conf import settings
from django.db import models

from accounts.models import Account


class Contact(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='contacts',
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='contacts',
    )
    name = models.CharField('Nome completo', max_length=150)
    email = models.EmailField('E-mail')
    phone = models.CharField('Telefone', max_length=20, blank=True)
    position = models.CharField('Cargo', max_length=120, blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'
        unique_together = ('owner', 'email')

    def __str__(self):
        return f'{self.name} ({self.account.name})'
