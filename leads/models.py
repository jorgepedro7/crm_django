from django.conf import settings
from django.db import models


class Lead(models.Model):
    class Status(models.TextChoices):
        NEW = 'novo', 'Novo'
        QUALIFIED = 'qualificado', 'Qualificado'
        CONVERTED = 'convertido', 'Convertido'
        LOST = 'perdido', 'Perdido'

    class Source(models.TextChoices):
        INBOUND = 'inbound', 'Inbound'
        OUTBOUND = 'outbound', 'Outbound'
        REFERRAL = 'indicacao', 'Indicação'
        EVENT = 'evento', 'Evento'
        OTHER = 'outro', 'Outro'

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='leads',
    )
    account = models.ForeignKey(
        'accounts.Account',
        on_delete=models.SET_NULL,
        related_name='leads',
        null=True,
        blank=True,
    )
    contact = models.ForeignKey(
        'contacts.Contact',
        on_delete=models.SET_NULL,
        related_name='leads',
        null=True,
        blank=True,
    )
    name = models.CharField('Nome do lead', max_length=150)
    email = models.EmailField('E-mail')
    phone = models.CharField('Telefone', max_length=20, blank=True)
    source = models.CharField(
        'Origem',
        max_length=20,
        choices=Source.choices,
        default=Source.INBOUND,
    )
    status = models.CharField(
        'Status',
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )
    notes = models.TextField('Observações', blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'
        unique_together = ('owner', 'email')

    def __str__(self):
        return self.name
