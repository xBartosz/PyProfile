from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


# class Author(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     slug = models.SlugField()
#
#     def __str__(self):
#         return self.user.username
#
#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.user.username)
#         return super().save(*args, **kwargs)

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_content = models.TextField(blank=False, null=False)
    post_date = models.DateTimeField(auto_now_add=True)

