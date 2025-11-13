from django.conf import settings
from django.db import models
from django.db.models import Max


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
    position = models.PositiveIntegerField('Posição', default=0)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'
        unique_together = ('owner', 'email')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if getattr(self, '_skip_position_auto', False):
            super().save(*args, **kwargs)
            return
        owner = getattr(self, 'owner', None)
        if not owner:
            super().save(*args, **kwargs)
            return
        previous_status = None
        if self.pk:
            previous_status = (
                Lead.objects.filter(pk=self.pk)
                .values_list('status', flat=True)
                .first()
            )
        if not self.pk or previous_status != self.status or self.position is None:
            max_position = (
                Lead.objects.filter(owner=owner, status=self.status)
                .exclude(pk=self.pk)
                .aggregate(max_pos=Max('position'))
                .get('max_pos')
            )
            next_position = (max_position or -1) + 1
            self.position = next_position
        super().save(*args, **kwargs)


class LeadStatus(models.Model):
    key = models.CharField(
        'Código',
        max_length=20,
        choices=Lead.Status.choices,
        unique=True,
    )
    label = models.CharField('Nome da coluna', max_length=50)
    order = models.PositiveSmallIntegerField('Ordem', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Coluna de Kanban'
        verbose_name_plural = 'Colunas de Kanban'

    def __str__(self):
        return self.label
