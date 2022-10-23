from django import template
from ..models import Message

register = template.Library()

@register.filter
def new_message(friend):
    exists = Message.objects.filter(from_user=friend, is_read=False).exists()
    if exists:
        return f"You've got new message"
    else:
        return ""



