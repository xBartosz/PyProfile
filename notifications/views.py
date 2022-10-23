from django.shortcuts import render
from .models import Notification


def notification_list(request):
    show_notifications = Notification.objects.filter(receiver=request.user)
    for notification in show_notifications:
        notification.is_seen = True
        notification.save()

    context = {'show_notifications': show_notifications}
    return render(request, 'notifications/notification_list.html', context)