import hashlib

from firebase_admin import auth
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from code_lighthouse_backend.models import AppUser
from code_lighthouse_backend.serializers import AppUserSerializer
from code_lighthouse_backend.validations.login_validations import login_validator

class AuthProvider(APIView):
    def post(self, request):

        try:
            id_token = request.data['idToken']
            email = request.data['email']

            username = request.data['username']
            photoURL = request.data['photoURL']

            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']

            try:
                user = AppUser.objects.get(email=email)
            except AppUser.DoesNotExist as e:
                user = AppUser(password='', username=username, email=email, provider=True, photoURL=photoURL)
                user.save()

            serialized_user = AppUserSerializer(user, context={'drill': True})
            refresh = RefreshToken.for_user(user)
            user_and_token = {
                "user": serialized_user.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            return Response(user_and_token, status=status.HTTP_200_OK)


        except Exception as e:
            return Response({'OK': False, 'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class Auth(APIView):
    def post(self, request):
        try:
            email = request.data['email']
            password = request.data['password']

            if login_validator["inputNull"] is False and (not email or len(email) == 0 or not password or len(password) == 0):
                return Response({'OK': False, 'data': 'E-mail or password is empty!'},
                                status=status.HTTP_400_BAD_REQUEST)

            if len(email) < login_validator["emailMin"]:
                return Response({'OK': False, 'data': 'E-mail is too short!'},
                                status=status.HTTP_400_BAD_REQUEST)

            if len(password) < login_validator["passwordMin"]:
                return Response({'OK': False, 'data': 'Password is too short!'},
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                user = AppUser.objects.get(email=email)
            except AppUser.DoesNotExist:
                try:
                    user = AppUser.objects.get(username=email)
                except AppUser.DoesNotExist as e:
                    return Response({'data': 'User does not exist!'}, status=status.HTTP_404_NOT_FOUND)

            # print(password, user.password)
            if user.password.strip() != '' and user.password == hashlib.sha256(password.encode('UTF-8')).hexdigest():

                serialized_user = AppUserSerializer(user, context={'drill': True})
                refresh = RefreshToken.for_user(user)
                user_and_token = {
                    "user": serialized_user.data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
                #
                return Response(user_and_token, status=status.HTTP_200_OK)
            else:
                if user.password.strip() == '':
                    return Response({'data': 'It appears this is a provider account! Maybe try Google or Github from down below?'}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({'data': 'Wrong credentials!'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

