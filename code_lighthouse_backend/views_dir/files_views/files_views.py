from rest_framework import status
from django.http import FileResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import os
from rest_framework_simplejwt.authentication import JWTAuthentication
from code_lighthouse_backend.models import  AppUser, Lighthouse
from code_lighthouse_backend.utils import  get_request_user_id






class ViewFile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, file_name, lighthouse_id):
        try:

            decoded_user_id = get_request_user_id(request)
            logged_in_user = AppUser.objects.get(id=decoded_user_id)

            lighthouse = Lighthouse.objects.get(id=lighthouse_id)


            if not lighthouse:
                return Response({'OK': False, 'data': 'This Lighthouse does not exist?'},
                                status=status.HTTP_404_NOT_FOUND)


            if logged_in_user not in lighthouse.people.all():
                return Response({'OK': False, 'data': 'You are not allowed to access this file!'},
                                status=status.HTTP_403_FORBIDDEN)
            # print(lighthouse.people.all(), file_name)

            if os.path.isfile(f'uploads/files/{file_name}'):
                return FileResponse(open(f'uploads/files/{file_name}', 'rb'))
            else:
                return Response({'OK': False, 'data': 'Could not find the file!'}, status=status.HTTP_404_NOT_FOUND)


        except Exception as e:
            return Response({'OK': False, 'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
