import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from threads.models import Thread

@receiver(post_delete, sender=Thread)
def delete_thread_cover_image(sender, instance, **kwargs):
    if instance.cover and hasattr(instance.cover, 'path'):
        try:
            os.remove(instance.cover.path)
        except FileNotFoundError:
            pass