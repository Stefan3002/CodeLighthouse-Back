import uuid

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from code_lighthouse_backend.models import AppUser, Lighthouse, Contest
from code_lighthouse_backend.serializers import LighthouseSerializer, LighthousePreviewSerializer, \
    ContestPreviewSerializer
from code_lighthouse_backend.utils import get_request_user_id

from code_lighthouse_backend.validations.join_lighthouse_validations import lighthouse_code_validator, \
    lighthouse_id_validator
from code_lighthouse_backend.validations.create_lighthouse_validation import lighthouse_name_validator, \
    lighthouse_description_validator


class GetLighthousePreview(APIView):
    def post(self, request):
        try:
            mode = request.GET.get('type')
            data = request.data
            enrollment_code = data['enrollmentCode']

            if mode == 'lighthouse':
                lighthouse = Lighthouse.objects.get(enrollment_code=enrollment_code)
                serialized_lighthouse = LighthousePreviewSerializer(lighthouse, context={'drill': False})
                return Response(serialized_lighthouse.data, status=status.HTTP_200_OK)
            else:
                if mode == 'contest':
                    contest = Contest.objects.get(enrollment_code=enrollment_code)
                    serialized_contest = ContestPreviewSerializer(contest, context={'drill': False})
                    return Response(serialized_contest.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'OK': False, 'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChangeEnrollLighthouse(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, lighthouseID):
        try:
            lighthouse = Lighthouse.objects.get(id=lighthouseID)

            decoded_user_id = get_request_user_id(request)
            logged_in_user = AppUser.objects.get(id=decoded_user_id)

            if logged_in_user == lighthouse.author:
                lighthouse.enrollment_code = uuid.uuid4()
                lighthouse.save()
                return Response({'OK': True, 'data': 'Enrollment code successfully generated!'},
                                status=status.HTTP_200_OK)
            else:
                return Response({'OK': False, 'data': 'You are not the owner of the Lighthouse!'},
                                status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'OK': False, 'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetEntity(APIView):
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
                return Response({'OK': False, 'data': 'You are not the owner of the Lighthouse!'},
                                status=status.HTTP_403_FORBIDDEN)
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
            decoded_user_id = get_request_user_id(request)
            userDB = AppUser.objects.get(id=decoded_user_id)
            enrollment_code = request.data['enrollment_code']

            if lighthouse_code_validator["inputNull"] is False and (not enrollment_code or len(enrollment_code) == 0):
                return Response({'OK': False, 'data': 'Enrollment code is missing!'},
                                status=status.HTTP_400_BAD_REQUEST)

            if len(enrollment_code) < lighthouse_code_validator["inputMin"]:
                return Response({'OK': False, 'data': 'Enrollment code is too short!'},
                                status=status.HTTP_400_BAD_REQUEST)

            mode = request.GET.get('type')
            if mode == 'lighthouse':
                entity = Lighthouse.objects.get(enrollment_code=enrollment_code)
            elif mode == 'contest':
                entity = Contest.objects.get(enrollment_code=enrollment_code)

            if lighthouse_id_validator["inputNull"] is False and not lighthouseID:
                return Response({'OK': False, 'data': 'ID is missing!'},
                                status=status.HTTP_400_BAD_REQUEST)

            if lighthouseID < lighthouse_id_validator["inputMin"]:
                return Response({'OK': False, 'data': 'ID is too short!'},
                                status=status.HTTP_400_BAD_REQUEST)

            if str(entity.enrollment_code) == enrollment_code:
                entity.people.add(userDB)
                return Response({}, status=status.HTTP_201_CREATED)
            else:
                raise Exception('Sorry, the entity did not respond for that access code. Are you sure you got it '
                                'right?')
        except ObjectDoesNotExist as e:
            return Response({'OK': False, 'data': 'This entity appears to be shut down? We could not find it!'},
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

            if lighthouse_name_validator["inputNull"] is False and (not name or len(name) == 0):
                return Response({'OK': False, 'data': 'Name of Lighthouse is missing!'},
                                status=status.HTTP_400_BAD_REQUEST)

            if len(name) < lighthouse_name_validator["inputMin"]:
                return Response({'OK': False, 'data': 'Name of Lighthouse too short!'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Check for duplicates!!!
            duplicate = Lighthouse.objects.filter(name=name)

            if (duplicate):
                return Response({'OK': False, 'data': 'Lighthouse with that name already exists!'},
                                status=status.HTTP_400_BAD_REQUEST)

            description = data['description']

            if lighthouse_description_validator["inputNull"] is False and (not description or len(description) == 0):
                return Response({'OK': False, 'data': 'Description of Lighthouse is missing!'},
                                status=status.HTTP_400_BAD_REQUEST)

            if len(description) < lighthouse_description_validator["inputMin"]:
                return Response({'OK': False, 'data': 'Description of Lighthouse too short!'},
                                status=status.HTTP_400_BAD_REQUEST)

            decoded_user_id = get_request_user_id(request)
            author = AppUser.objects.get(id=decoded_user_id)

            community = data['community']

            new_lighthouse = Lighthouse(name=name, description=description, author=author, public=community)
            new_lighthouse.save()
            new_lighthouse.people.add(author)
            return Response({'OK': True, 'data': 'Created your Lighthouse!'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'OK': False, 'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
