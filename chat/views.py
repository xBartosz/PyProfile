# from django.shortcuts import render
# from website.models import MyUser
# from .models import Message
#
# # Create your views here.
#
#
# def chat(request):
#     friends = request.user.friends.all()
#
#     context = {'friends' : friends}
#
#     return render(request, 'chat/chat.html', context)
#
# def send_message(request, user_name):
#     usr = MyUser.objects.get(user_name=user_name)
#     msg_from_other = Message.objects.filter(message_from_user = usr, message_to_user = request.user)
#     msg_from_me = Message.objects.filter(message_from_user = request.user, message_to_user = usr)
#     context = {'usr':usr, 'msg_from_other' : msg_from_other, 'msg_from_me' : msg_from_me}
#     return render(request, 'chat/chat2.html', context)
from django.shortcuts import render, redirect
from django.views import View
from website.models import MyUser
from django.db.models import Q
from .serializers import MessageSerializer
from .models import Message, Thread
from website.serializers import UserSerializer
from users.models import Profile


def chat(request):
    friends = request.user.friends.all().order_by('first_name')

    context = {'friends' : friends}

    return render(request, 'chat/chat.html', context)
class ChatIndexView(View):
    template_name = 'chat/chatroom.html'

    def get_chats(self, me, friend):
        thread_obj = None
        try:
            thread_obj = Thread.objects.get((Q(user1=me) & Q(user2=friend)) | (Q(user1=friend) & Q(user2=me)))
            return Message.objects.order_by('timestamp').filter(thread=thread_obj)
        except:
            return None

    def get(self, request, friend):
        user = request.user

        context = {}
        if user.is_authenticated:
            serialized_data = UserSerializer(user)
            friend_obj = MyUser.objects.get(user_name=friend)
            friend_profile = Profile.objects.get(user=friend_obj)

            friend_serialized_data = UserSerializer(friend_obj)
            all_chats = self.get_chats(user, friend_obj)

            if all_chats is not None:
                chat_serialized_data = MessageSerializer(all_chats, many=True)

                context = {
                    'me': serialized_data.data,
                    'friend': friend_serialized_data.data,
                    'chats': chat_serialized_data.data,
                    'friend_profile': friend_profile
                }
            else:
                context = {
                    'me': serialized_data.data,
                    'friend': friend_serialized_data.data,
                    'chats': ''
                }

            return render(request, 'chat/chat2.html', context)
        return redirect('login')