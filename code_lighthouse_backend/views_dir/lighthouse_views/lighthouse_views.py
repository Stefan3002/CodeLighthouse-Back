from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from code_lighthouse_backend.models import AppUser, Lighthouse
from code_lighthouse_backend.serializers import LighthouseSerializer


class GetLighthouse(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, lighthouseID):
        try:
            lighthouse = Lighthouse.objects.get(id=lighthouseID)
            serialized_lighthouse = LighthouseSerializer(lighthouse, context={'drill': False})
            return Response(serialized_lighthouse.data, status=status.HTTP_200_OK)
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
        data = request.data
        name = data['name']
        description = data['description']
        user_id = data['user_id']
        author = AppUser.objects.filter(user_id=user_id)[0]
        new_lighthouse = Lighthouse(name=name, description=description, author=author)
        new_lighthouse.save()
        new_lighthouse.people.add(author)
        return Response({}, status=status.HTTP_201_CREATED)
