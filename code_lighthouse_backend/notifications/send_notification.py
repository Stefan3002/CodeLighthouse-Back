from code_lighthouse_backend.models import Lighthouse, Notification

def send_notification(text_data):
    message = text_data

    if message['type'] == 'new_announcement':
        lighthouse_id = message['lighthouseId']
        lighthouse = Lighthouse.objects.get(id=lighthouse_id)

        for person in lighthouse.people.all():
            new_notification = Notification(user=person, content=message['message'], url=message['url'])
            new_notification.save()