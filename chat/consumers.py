from channels.generic.websocket import AsyncWebsocketConsumer
from website.models import MyUser
from django.db.models import Q
from asgiref.sync import sync_to_async, async_to_sync
import json
from .models import Message, Thread
from website.serializers import UserSerializer


class ChatConsumer(AsyncWebsocketConsumer):

    @sync_to_async
    def get_message_queryset(self, thread):
        try:
            return list(Message.objects.all().filter(thread=thread).update(is_read=True))
        except:
            pass

    async def connect(self):
        user = self.scope['user']     # logged in user
        friend = await sync_to_async(MyUser.objects.get, thread_sensitive=True)(user_name=self.scope['url_route']['kwargs']['friend'])    # get user object of friend


        # create a new Thread object if thread of specific chat does not exists, otherwise return the thread
        thread = None
        try:
            thread = await sync_to_async(Thread.objects.get, thread_sensitive=True)((Q(user1=user) & Q(user2=friend)) | (Q(user1=friend) & Q(user2=user)))
        except:
            thread = await sync_to_async(Thread.objects.create, thread_sensitive=True)(user1=user, user2=friend)
        finally:
            self.room_name = thread.room_name   # room name

        await self.get_message_queryset(thread) # update is_read property to true of messages

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        '''
        disconnect the websocket connection.
        '''
        await self.channel_layer.group_discard (
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        payload = json.loads(text_data)
        from_user = await sync_to_async(MyUser.objects.get, thread_sensitive=True)(user_name=payload['user']['user_name'])    # get user object of friend
        to_user = await sync_to_async(MyUser.objects.get, thread_sensitive=True)(user_name=payload['friend']['user_name'])    # get user object of friend

        thread_obj = await sync_to_async(Thread.objects.get, thread_sensitive=True)((Q(user1=from_user) & Q(user2=to_user)) | (Q(user1=to_user) & Q(user2=from_user)))

        message_instance = await sync_to_async(Message.objects.create, thread_sensitive=True)(message_body=payload['message'], from_user=from_user, to_user=to_user, thread=thread_obj)

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chatroom_messages',
                'message': message_instance.message_body,
                'user': message_instance.from_user
            }
        )

    async def chatroom_messages(self, event):
        user_serialized_data = UserSerializer(event['user'])

        await self.send(text_data=json.dumps({
            'message': event['message'],
            'user': user_serialized_data.data
        }))