from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.


class Friend_Request(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='to_user')

    def __str__(self):
        return (f'From {self.from_user}, to {self.to_user}')

