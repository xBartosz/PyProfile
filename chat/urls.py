from django.urls import path
from .views import chat, ChatIndexView

urlpatterns = [
    path('chat/', chat, name='chat'),
    path('chatroom/<str:friend>/', ChatIndexView.as_view(), name='chatroom'),
]
