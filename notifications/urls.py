from django.urls import path
from .views import notification_list, mark_as_read, delete_all_notifications


urlpatterns = [
    path('notifications/', notification_list, name='notification_list'),
    path('notifications/mark_as_read', mark_as_read, name='mark_as_read'),
    path('notifications/delete_all', delete_all_notifications, name='delete_all_notifications')

]