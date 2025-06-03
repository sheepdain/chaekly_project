import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_delete, sender=User)
def delete_user_profile_image(sender, instance, **kwargs):
    if instance.profile_image and hasattr(instance.profile_image, 'path'):
        try:
            os.remove(instance.profile_image.path)
        except FileNotFoundError:
            pass
