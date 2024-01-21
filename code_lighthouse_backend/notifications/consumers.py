import json
from urllib.parse import parse_qs

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from code_lighthouse_backend.models import AppUser, Lighthouse, Notification
from code_lighthouse_backend.utils import get_request_user_id


class NotificationConsumer(WebsocketConsumer):
    def connect(self):

        self.rooms = []

        search_params = parse_qs(self.scope['query_string'].decode())
        user_token = search_params['user'][0]

        decoded_user_id = get_request_user_id(None, user_token, True)
        logged_in_user = AppUser.objects.get(id=decoded_user_id)

        # Add user to all of his Lighthouses rooms

        for lighthouse in logged_in_user.enrolled_Lighthouses.all():
            room_name = f'lighthouse-{lighthouse.id}'
            self.rooms.append(room_name)
            async_to_sync(self.channel_layer.group_add)(
                room_name, self.channel_name
            )

        self.accept()
        self.send(text_data=json.dumps({
            'type': 'connected',
            'content': 'CONNECTED!!',
            'id': '1',
            'read': False
        }))

    def disconnect(self, code):
        for room in self.rooms:
            async_to_sync(self.channel_layer.group_discard)(
                room, self.channel_name
            )

    def receive(self, text_data):
        message = json.loads(text_data)
        print(message)

        if message['type'] == 'new_announcement':
            lighthouse_id = message['lighthouseId']
            lighthouse = Lighthouse.objects.get(id=lighthouse_id)

            room_name = f'lighthouse-{lighthouse.id}'

            for person in lighthouse.people.all():
                new_notification = Notification(user=person, content=message['message'], url=message['url'])
                new_notification.save()

            async_to_sync(self.channel_layer.group_send)(
                room_name,
                {
                    'type': 'notification',
                    'content': message['message'],
                    'url': message['url']
                    # 'id': new_notification.id
                }
            )

    def notification(self, text_data):
        self.send(text_data=json.dumps(text_data))
