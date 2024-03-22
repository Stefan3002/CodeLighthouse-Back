from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from code_lighthouse_backend.models import AppUser
from code_lighthouse_backend.serializers import LighthouseSerializer, ChallengeSerializer, ContestSerializer
from code_lighthouse_backend.utils import get_request_user_id


class GetUserEntity(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            data = request.data

            decoded_user_id = get_request_user_id(request)
            logged_in_user = AppUser.objects.get(id=decoded_user_id)

            type = request.GET.get('type')
            start_index = int(request.GET.get('start'))
            end_index = int(request.GET.get('end'))

            if type == 'lighthouses':
                if end_index != -1:
                    entities = logged_in_user.enrolled_Lighthouses.all()[start_index:end_index]
                else:
                    entities = logged_in_user.enrolled_Lighthouses.all()
                serialized_entities = LighthouseSerializer(entities, many=True)
            elif type == 'challenges':
                if end_index != -1:
                    entities = logged_in_user.solved_challenges.all()[start_index:end_index]
                else:
                    entities = logged_in_user.solved_challenges.all()
                serialized_entities = ChallengeSerializer(entities, many=True)
            elif type == 'contests':
                if end_index != -1:
                    entities1 = logged_in_user.contests.all()
                    entities2 = logged_in_user.authored_contests.all()
                    entities = entities2.union(entities1)[start_index:end_index]
                else:
                    entities1 = logged_in_user.contests.all()
                    entities2 = logged_in_user.authored_contests.all()
                    entities = entities1.union(entities2)
                serialized_entities = ContestSerializer(entities, many=True)

            return Response(serialized_entities.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)