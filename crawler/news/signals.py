from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Website


@receiver(pre_save, sender=Website)
def setup_scraper(sender, instance, **kwargs):
    instance.update_job()
