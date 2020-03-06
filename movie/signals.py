import os

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from movie.models import Movie


@receiver(post_delete, sender=Movie)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Movie` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_save, sender=Movie)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Movie` object is updated
    with new image.
    """
    if not instance.pk:
        return False

    try:
        old_file = Movie.objects.get(pk=instance.pk).image
    except Movie.DoesNotExist:
        return False

    new_image = instance.image
    if not old_file == new_image:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
