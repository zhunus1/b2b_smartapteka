import os
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete
from .models import Document
# These two auto-delete files from filesystem when they are unneeded:

@receiver(post_delete, sender=Document)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Document` object is deleted.
    """
    if instance.document:
        if os.path.isfile(instance.document.path):
            os.remove(instance.document.path)

@receiver(pre_save, sender=Document)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Document` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Document.objects.get(pk=instance.pk).document
    except Document.DoesNotExist:
        return False

    new_file = instance.document
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)