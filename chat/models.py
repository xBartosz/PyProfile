from django.db import models
from datetime import datetime
from website.models import MyUser
from django.utils import timezone
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db.models import Q


class Thread(models.Model):
    user1 = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_one')
    user2 = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_two')
    unique_room_id = models.CharField(max_length=10, null=True, blank=True)
    room_name = models.CharField(max_length=50, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def create_new_room(self):
        self.room_name = f'{self.user1.user_name}-{self.unique_room_id}-{self.user2.user_name}'
        self.save()

    def __str__(self):
        return self.room_name

    class Meta:
        verbose_name = 'Thread'
        verbose_name_plural = 'Threads'


def unique_room_id_generator(sender, instance, *args, **kwargs):
    from PyProfile.custom_functions import unique_room_genarator
    if not instance.unique_room_id:
        instance.unique_room_id = unique_room_genarator(instance)

pre_save.connect(unique_room_id_generator, sender=Thread)

@receiver(post_save, sender=Thread)
def create_room_name(sender, instance, created, **kwargs):
    if created:
        instance.create_new_room()

class Message(models.Model):
    messag_body = models.TextField(default="empty")
    from_user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='to_user')
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'