from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from . import models


@receiver(pre_save, sender=models.SubjectModel)
def generate_slug_for_subject(sender, instance, **kwargs):
    if instance.pk:
        previous = models.SubjectModel.objects.get(pk=instance.pk)
        if previous.title == instance.title:
            return

    original_slug = slugify(instance.title)
    slug = original_slug
    count = 1

    while models.SubjectModel.objects.filter(slug=slug).exists():
        slug = f"{original_slug}-{count}"
        count += 1
    instance.slug = slug


@receiver(pre_save, sender=models.GroupModel)
def generate_slug_for_group(sender, instance, **kwargs):
    if instance.pk:
        previous = models.GroupModel.objects.get(pk=instance.pk)
        if previous.title == instance.title:
            return

    original_slug = slugify(instance.title)
    slug = original_slug
    count = 1

    while models.GroupModel.objects.filter(slug=slug).exists():
        slug = f"{original_slug}-{count}"
        count += 1
    instance.slug = slug
