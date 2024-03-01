import hashlib

from firebase_admin import auth
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from code_lighthouse_backend.models import AppUser
from code_lighthouse_backend.serializers import AppUserSerializer


class AuthProvider(APIView):
    def post(self, request):

        try:
            # default_app = firebase_admin.initialize_app()
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
            try:
                user = AppUser.objects.get(email=email)
            except AppUser.DoesNotExist:
                user = AppUser.objects.get(username=email)
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

