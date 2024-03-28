import os

from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from code_lighthouse_backend.email_sending.messages import new_announcement_message, format_new_announcement_email
from code_lighthouse_backend.email_sending.send_emails import send_email
from code_lighthouse_backend.models import AppUser, Lighthouse, Announcement
from code_lighthouse_backend.utils import get_request_user_id
from code_lighthouse_backend.validations.create_announcement_validation import announcement_content_validator


class Announcements(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            lighthouse_id = data['lighthouseId']
            content = data['content']
            files = data['files']

            if files == 'undefined':
                files = None

            if announcement_content_validator["inputNull"] is False and (not content or len(content) == 0):
                return Response({'OK': False, 'data': 'Announcement is missing!'},
                                status=status.HTTP_400_BAD_REQUEST)

            if len(content) < announcement_content_validator["inputMin"]:
                return Response({'OK': False, 'data': 'Announcement is too short!'},
                                status=status.HTTP_400_BAD_REQUEST)

            decoded_user_id = get_request_user_id(request)
            logged_in_user = AppUser.objects.get(id=decoded_user_id)
            lighthouse = Lighthouse.objects.get(id=lighthouse_id)

            if not logged_in_user == lighthouse.author:
                return Response({"data": 'You are not the owner of this Lighthouse!'}, status=status.HTTP_403_FORBIDDEN)
            if len(content.strip()) < 15:
                return Response({"data": 'Too short announcement!'}, status=status.HTTP_400_BAD_REQUEST)

            new_announcement = Announcement(file=files, lighthouse=lighthouse, author=logged_in_user, content=content)
            new_announcement.save()

            # Send E-mails.
            for receiver in lighthouse.people.all():
                format_new_announcement_email(receiver.username, lighthouse.name, content)
                send_email(receiver_email=receiver.email, message=new_announcement_message)

            return Response({"data": 'Successfully created!'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, announcement_id):
        try:
            decoded_user_id = get_request_user_id(request)
            logged_in_user = AppUser.objects.get(id=decoded_user_id)

            announcement = Announcement.objects.get(id=announcement_id)

            if logged_in_user == announcement.author:
                with transaction.atomic():
                    if os.path.isfile(f'{announcement.file}'):
                        os.remove(f'{announcement.file}')
                    announcement.delete()
                return Response({'OK': True, 'data': 'Successfully deleted!'}, status=status.HTTP_200_OK)
            else:
                return Response({'OK': False, 'data': 'This is not your announcement!'},
                                status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'OK': False, 'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
