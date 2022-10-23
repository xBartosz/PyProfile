from django.db import models


class Notification(models.Model):
    NOTIFICATION_TYPES = [("Like", "Like"), ("Comment", "Comment"), ("Post", "Post")]

    post = models.ForeignKey('website.Post', on_delete=models.CASCADE, related_name="notif_post", blank=True, null=True)
    sender = models.ForeignKey('website.MyUser', on_delete=models.CASCADE, related_name="notif_from_user")
    receiver = models.ForeignKey('website.MyUser', on_delete=models.CASCADE, related_name="notif_to_user")
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    notification_text = models.CharField(max_length=50, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)