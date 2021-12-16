from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import News


@receiver(pre_save, sender=News)
def generate_regex(sender, instance, **kwargs):
    instance.generate_category_regex()
    instance.generate_item_regex()
