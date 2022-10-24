from django import template
from notifications.models import Notification
from friends.models import FriendRequest
from chat.models import Message

register = template.Library()


@register.filter
def number_of_friend_requests(user):
    return len(FriendRequest.objects.filter(request_to_user=user))


@register.filter
def number_of_new_messages(user):
    return len(Message.objects.filter(to_user=user, is_read=False))


@register.filter
def number_of_notifications(user):
    return len(Notification.objects.filter(receiver=user, is_seen=False))