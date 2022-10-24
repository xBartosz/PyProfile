from django.shortcuts import render, redirect
from .models import Notification
import time


def notification_list(request):
    show_notifications_seen = Notification.objects.filter(receiver=request.user, is_seen=True).order_by('-date')
    show_notifications = Notification.objects.filter(receiver=request.user, is_seen=False).order_by('-date')
    show_notifications_amount = len(show_notifications_seen) + len(show_notifications)

    context = {'show_notifications_seen': show_notifications_seen,
               'show_notifications': show_notifications,
               'show_notifications_amount': show_notifications_amount}
    return render(request, 'notifications/notification_list.html', context)

def mark_as_read(request):
    show_notifications = Notification.objects.filter(receiver=request.user)
    for notification in show_notifications:
        notification.is_seen = True
        notification.save()
    return redirect(request.META['HTTP_REFERER'])

def delete_all_notifications(request):
    Notification.objects.filter(receiver=request.user).delete()
    return redirect(request.META['HTTP_REFERER'])
