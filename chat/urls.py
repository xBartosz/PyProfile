from django.urls import path
from .views import chat, ChatIndexView

urlpatterns = [
    path('chat/', chat, name='chat'),
    # path('chat/chat_with/<str:user_name>', send_message, name='chat_send_message'),
    path('chatroom/<str:friend>/', ChatIndexView.as_view(), name='chatroom'),
]
