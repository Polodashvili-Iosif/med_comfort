from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from unidecode import unidecode

from .models import Service, ServiceCategory


@receiver(pre_save, sender=ServiceCategory)
def set_slug_for_service_category(sender, instance, **kwargs):
    instance.slug = slugify(unidecode(instance.name))


@receiver(pre_save, sender=Service)
def set_slug_for_service(sender, instance, **kwargs):
    instance.slug = slugify(unidecode(instance.name))
