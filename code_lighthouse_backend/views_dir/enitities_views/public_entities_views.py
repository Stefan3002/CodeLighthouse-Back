from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from code_lighthouse_backend.models import Lighthouse, Contest
from code_lighthouse_backend.serializers import LighthouseSerializer, ContestSerializer

from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView


class PublicEntities(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            mode = request.GET.get('type')
            if mode == 'lighthouse':
                start_index = int(request.GET.get('start'))
                end_index = int(request.GET.get('end'))
                communities = Lighthouse.objects.filter(public=True)[start_index:end_index]
                serialized_lighthouses = LighthouseSerializer(communities, many=True)
                return Response(serialized_lighthouses.data, status=status.HTTP_200_OK)
            if mode == 'contest':
                communities = Contest.objects.filter(public=True)
                serialized_contests = ContestSerializer(communities, many=True)
                return Response(serialized_contests.data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)