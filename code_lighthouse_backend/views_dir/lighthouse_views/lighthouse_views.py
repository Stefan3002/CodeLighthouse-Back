from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from code_lighthouse_backend.models import AppUser, Lighthouse
from code_lighthouse_backend.serializers import LighthouseSerializer
from code_lighthouse_backend.utils import get_request_user_id


class GetLighthouse(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, lighthouseID):
        try:
            lighthouse = Lighthouse.objects.get(id=lighthouseID)

            decoded_user_id = get_request_user_id(request)
            logged_in_user = AppUser.objects.get(id=decoded_user_id)

            if logged_in_user == lighthouse.author:
                lighthouse.archived = True
                lighthouse.save()
                return Response({'OK': True, 'data': 'Successfully archived!'}, status=status.HTTP_200_OK)
            else:
                return Response({'OK': False, 'data': 'You are not the owner of the Lighthouse!'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'OK': False, 'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, lighthouseID):
        try:
            lighthouse = Lighthouse.objects.get(id=lighthouseID)
            decoded_user_id = get_request_user_id(request)
            logged_in_user = AppUser.objects.get(id=decoded_user_id)

            if logged_in_user in lighthouse.people.all():
                serialized_lighthouse = LighthouseSerializer(lighthouse, context={'drill': False})
                return Response(serialized_lighthouse.data, status=status.HTTP_200_OK)
            else:
                raise Exception('This lighthouse does not recognize you. Are you enrolled here?')
        except Exception as e:
            return Response({'OK': False, 'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, lighthouseID):
        try:
            userID = request.data['user_id']
            enrollment_code = request.data['enrollment_code']
            userDB = AppUser.objects.get(user_id=userID)
            lighthouse = Lighthouse.objects.get(id=lighthouseID)

            if str(lighthouse.enrollment_code) == enrollment_code:
                lighthouse.people.add(userDB)
                return Response({}, status=status.HTTP_201_CREATED)
            else:
                raise Exception('Sorry, the lighthouse did not respond for that access code. Are you sure you got it '
                                'right?')
        except ObjectDoesNotExist as e:
            return Response({'OK': False, 'data': 'This lighthouse appears to be shut down? We could not find it!'},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'OK': False, 'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetLighthouses(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, lower_limit, upper_limit):
        try:
            lighthouses = Lighthouse.objects.all()[lower_limit: upper_limit]
            serialized_lighthouses = LighthouseSerializer(lighthouses, many=True)
            return Response(serialized_lighthouses.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'OK': False, 'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateLighthouse(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            name = data['name']
            description = data['description']
            user_id = data['user_id']
            community = data['community']

            author = AppUser.objects.get(user_id=user_id)
            new_lighthouse = Lighthouse(name=name, description=description, author=author, public=community)
            new_lighthouse.save()
            new_lighthouse.people.add(author)
            return Response({'OK': True, 'data': 'Created your Lighthouse!'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'OK': False, 'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
