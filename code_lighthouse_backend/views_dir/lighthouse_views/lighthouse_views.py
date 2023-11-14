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
        lighthouse = Lighthouse.objects.get(id=lighthouseID)
        serialized_lighthouse = LighthouseSerializer(lighthouse, context={'drill': False})
        return Response(serialized_lighthouse.data, status=status.HTTP_200_OK)

    def post(self, request, lighthouseID):
        userID = request.data['user_id']
        enrollment_code = request.data['enrollment_code']
        userDB = AppUser.objects.filter(user_id=userID)[0]
        lighthouse = Lighthouse.objects.filter(id=lighthouseID)[0]

        print(lighthouse.enrollment_code, enrollment_code)
        if str(lighthouse.enrollment_code) == enrollment_code:
            lighthouse.people.add(userDB)
            return Response({}, status=status.HTTP_201_CREATED)
        else:
            return Response({'data': 'Sorry, the codes do not match!'}, status=status.HTTP_401_UNAUTHORIZED)

class GetLighthouses(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, lower_limit, upper_limit):
        lighthouses = Lighthouse.objects.all()[lower_limit: upper_limit]
        serialized_lighthouses = LighthouseSerializer(lighthouses, many=True)
        return Response(serialized_lighthouses.data, status=status.HTTP_200_OK)



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