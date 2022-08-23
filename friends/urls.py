from django.urls import path
from .views import send_friend_request, decline_friend_request, accept_friend_request, cancel_friend_request, delete_friend

urlpatterns = [
    path('send_friend_request/<int:id>', send_friend_request, name="send_friend_request"),
    path('decline_friend_request/<int:id>', decline_friend_request, name="decline_friend_request"),
    path('accept_friend_request/<int:id>', accept_friend_request, name="accept_friend_request"),
    path('cancel_friend_request/<int:id>', cancel_friend_request, name="cancel_friend_request"),
    path('delete_friend/<int:id>', delete_friend, name="delete_friend"),

]