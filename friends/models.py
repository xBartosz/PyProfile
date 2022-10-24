from django.db import models
from django.conf import settings


class FriendRequest(models.Model):
    request_from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='request_from_user')
    request_to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='request_to_user')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'From {self.request_from_user}, to {self.request_to_user}'

