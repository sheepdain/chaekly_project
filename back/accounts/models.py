from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid, os
from PIL import Image

def user_profile_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4().hex}.{ext}'
    return os.path.join('profile', filename)


class User(AbstractUser):
    gender = models.CharField(max_length=1, choices=[('M', '남성'), ('F', '여성')])
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=15, unique=True)
    profile_image = models.ImageField(upload_to=user_profile_path, blank=True)
    introduction = models.TextField(max_length=500, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)

    wishlist = models.ManyToManyField(
        'books.Book',
        related_name='wishlisted_users',
        blank=True
    )

    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
    )


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.profile_image:
            image_path = self.profile_image.path
            img = Image.open(image_path)

            max_size = (300, 300)   # 최대 크기
            img.thumbnail(max_size) # 비율 유지하며 축소
            img.save(image_path)

    def __str__(self):
      return f'{self.nickname} ({self.username})'
    



