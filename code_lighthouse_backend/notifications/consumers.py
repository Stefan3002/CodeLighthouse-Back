import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = 'room1'

        print(self.scope['user'])
        async_to_sync(self.channel_layer.group_add)(
            self.room_name, self.channel_name
        )

        self.accept()
        self.send(text_data=json.dumps({
            'type': 'connected',
            'message': 'CONNECTED!!'
        }))
    def disconnect(self, code):
        print('NOMORE!')

    def receive(self, text_data):
        message = json.loads(text_data)
        print(message)
        if message['type'] == 'new_announcement':
            async_to_sync(self.channel_layer.group_send)(
                self.room_name,
                {
                    'type': 'notification',
                    'message': message['message']
                }
            )

    def notification(self, text_data):
        self.send(text_data=json.dumps(text_data))