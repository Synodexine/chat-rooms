import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

from chat.models import Room


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        try:
            token = {'token': self.scope['query_string'][15:]}
            validated_data = VerifyJSONWebTokenSerializer().validate(token)
            self.scope['user'] = validated_data['user']
        except:
            self.close()
            return

        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        try:
            self.scope['room'] = Room.objects.get(id=self.room_id)
            self.scope['room'].users_online.add(self.scope['user'].client)
        except Room.DoesNotExist:
            self.close()
            return

        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()
        self.send_message('joined the chat.')

    def disconnect(self, code):
        self.scope['room'].users_online.remove(self.scope['user'].client)
        self.send_message('left the chat.')
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.send_message(message)

    def send_message(self, value: str):
        async_to_sync(self.channel_layer.group_send)(
            group=self.room_group_name,
            message={
                'type': 'chat_message',
                'message': value,
                'username': self.scope['user'].username,
            }
        )

    def chat_message(self, event):
        text_data = json.dumps({
            'message': event['message'],
            'username': event['username'],
        })

        self.send(text_data=text_data)
