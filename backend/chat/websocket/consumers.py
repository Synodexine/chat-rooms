import json
from channels.generic.websocket import WebsocketConsumer
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        self.channel_layer.group_add(self.room_group_name, self.channel_name)
        try:
            print(self.scope)
            token = {'token': self.scope['cookies']['token'].split('%20')[1]}
            validated_data = VerifyJSONWebTokenSerializer().validate(token)
            print(validated_data['user'])
            self.accept()
        except KeyError:
            self.close()

    def disconnect(self, code):
        self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.channel_layer.group_send(
            group=self.room_group_name,
            message={
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        text_data = json.dumps(
            {'message': event['message']}
        )

        self.send(text_data=text_data)
