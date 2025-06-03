from django.db import models
from django.conf import settings
from books.models import Book

User = settings.AUTH_USER_MODEL

class Thread(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='threads')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='threads')
    reading_time = models.PositiveIntegerField(default=0)
    read_date = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=100)
    cover = models.ImageField(upload_to="threads/covers/", null=True, blank=True)
    content = models.TextField()
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(User, blank=True, related_name='like_threads')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)