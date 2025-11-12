from django.conf import settings
from django.db import models


class Account(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='accounts',
    )
    name = models.CharField('Nome da empresa', max_length=150)
    industry = models.CharField('Segmento', max_length=100, blank=True)
    city = models.CharField('Cidade', max_length=100, blank=True)
    website = models.URLField('Site', blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'
        unique_together = ('owner', 'name')

    def __str__(self):
        return self.name
