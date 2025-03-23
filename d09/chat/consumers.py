# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from .models import Room, Message
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    # this function will be called when a new websocket connection is established
    async def connect(self):
        self.slug = self.scope['url_route']['kwargs']['slug']
        self.room_group_name = f'chat_{self.slug}'

        # Roomが実在するか確認 (存在しない場合は close)
        # シンプルにここではエラー無視でも可
        try:
            self.room = await self.get_room(self.slug)
        except Room.DoesNotExist:
            await self.close()
            return

        # Groupに参加
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # ログインユーザ名を取得(非同期対応)
        user = self.scope["user"] if self.scope["user"].is_authenticated else AnonymousUser()
        self.username = user.username if user.is_authenticated else "Anonymous"

        await self.accept()

        # 最新の3件のメッセージを取得して送信
        last_messages = await self.get_last_3_messages(self.room)
        for msg in last_messages:
            await self.send(text_data=json.dumps({
                'message': f"{msg.user}: {msg.content}"
            }))

        # 入室メッセージを全員に通知
        join_text = f"{self.username} has joined the chat"
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': join_text,
            }
        )

    async def disconnect(self, close_code):
        # 退出メッセージを送信
        leave_text = f"{self.username} has left the chat"
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': leave_text,
            }
        )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')

        # 受け取ったメッセージを同じグループにブロードキャスト
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f"{self.username}: {message}",
            }
        )
        # DBにメッセージを保存
        await self.save_message(self.room, self.username, message)

    async def chat_message(self, event):
        message = event['message']
        # WebSocket に送信
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @staticmethod
    @sync_to_async
    def get_room(slug):
        # this is to check if the room exists when a new connection is established
        return Room.objects.get(slug=slug)

    @staticmethod
    @sync_to_async
    def get_last_3_messages(room):
        return list(Message.objects.filter(room=room).order_by('-timestamp')[:3][::-1])

    @staticmethod
    @sync_to_async
    def save_message(room, user, content):
        Message.objects.create(room=room, user=user, content=content)