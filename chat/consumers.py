import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    @database_sync_to_async
    def save_message(self, user, room, content):
        return Message.objects.create(user=user, room=room, content=content)

    @database_sync_to_async
    def get_message(self, message_id):
        try:
            return Message.objects.select_related('user').get(id=message_id)
        except Message.DoesNotExist:
            return None

    @database_sync_to_async
    def delete_message(self, message_id):
        Message.objects.filter(id=message_id).delete()

    async def receive(self, text_data):
        data = json.loads(text_data)

        if 'message' in data:
            message = data['message']
            user = self.scope["user"]
            new_message = await self.save_message(user, self.room_name, message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': f'{user.username}: {message}',
                    'message_id': new_message.id,
                    'user_id': self.scope["user"].id 
                }
            )

        elif 'typing' in data:
            username = self.scope["user"].username
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_typing',
                    'username': username,
                }
            )

        elif 'delete_message' in data:
            message_id = data['delete_message']
            requester = self.scope["user"]

            message = await self.get_message(message_id)
            if message:
                print(f"[DELETE DEBUG] Owner: {message.user.id}, Requester: {requester.id}")
                if message.user.id == requester.id:
                    await self.delete_message(message_id)
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'message_deleted',
                            'message_id': message_id
                        }
                    )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'message_id': event['message_id'],
            'user_id': event['user_id']
        }))

    async def message_deleted(self, event):
        await self.send(text_data=json.dumps({
            'message_deleted': event['message_id']
        }))

    async def user_typing(self, event):
        await self.send(text_data=json.dumps({
            'typing': f"{event['username']} is typing..."
        }))
