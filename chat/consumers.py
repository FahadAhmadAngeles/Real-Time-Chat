import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_group_name = "chat_room"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        message = data["message"]
        username = data["username"]

        #  SAVE TO DATABASE 
        await self.save_message(username, message)

        #  BROADCAST TO ALL USERS
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "username": event["username"]
        }))

    # ✅ helper function for DB write
    @database_sync_to_async
    def save_message(self, username, message):
        return Message.objects.create(
            username=username,
            content=message
        )