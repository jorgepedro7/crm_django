from django.dispatch import Signal, receiver

from .models import Lead

lead_converted = Signal()


@receiver(lead_converted)
def set_lead_as_converted(sender, lead, **kwargs):
    if lead.status != Lead.Status.CONVERTED:
        lead.status = Lead.Status.CONVERTED
        lead.save(update_fields=['status', 'updated_at'])
