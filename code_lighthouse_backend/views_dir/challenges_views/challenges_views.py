from django.db import transaction
from django.db.models import Q
from django.utils.text import slugify
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from code_lighthouse_backend.email_sending.messages import format_new_admin_email, new_admin_message
from code_lighthouse_backend.email_sending.send_emails import send_email_async, send_email
from code_lighthouse_backend.models import Challenge, AppUser, Code, Reports, Like
from code_lighthouse_backend.serializers import ChallengeSerializer
from code_lighthouse_backend.utils import get_request_user_id

from code_lighthouse_backend.validations.create_challenge_validations import challenge_name_validator, challenge_description_validator, challenge_randomFunction_validator, challenge_hardFunction_validator, challenge_trueFunction_validator


class PostChallenge(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self):
        pass

    def post(self, request):
        try:
            data = request.data
            title = data['title']
            time_limit = data['timeLimit']


            if challenge_name_validator["inputNull"] is False and (not title or len(title) == 0):
                return Response({'OK': False, 'data': 'Name of Challenge is missing!'},
                            status=status.HTTP_400_BAD_REQUEST)

            if len(title) < challenge_name_validator["inputMin"]:
                return Response({'OK': False, 'data': 'Name of Challenge is too short!'},
                            status=status.HTTP_400_BAD_REQUEST)

            # Check for duplicates!!!
            duplicate = Challenge.objects.filter(title=title)
            if (duplicate):
                return Response({'OK': False, 'data': 'Challenge with that name already exists!'},
                        status=status.HTTP_400_BAD_REQUEST)


            description = data['description']

            if challenge_description_validator["inputNull"] is False and (not description or len(description) == 0):
                return Response({'OK': False, 'data': 'Description of Challenge is missing!'},
                            status=status.HTTP_400_BAD_REQUEST)

            if len(description) < challenge_description_validator["inputMin"]:
                return Response({'OK': False, 'data': 'Description of Challenge is too short!'},
                            status=status.HTTP_400_BAD_REQUEST)

            true_function = data['trueFunction']

            if challenge_trueFunction_validator["inputNull"] is False and (not true_function or len(true_function) == 0):
                return Response({'OK': False, 'data': 'The True function of the Challenge is missing!'},
                            status=status.HTTP_400_BAD_REQUEST)

            random_function = data['randomFunction']

            if challenge_randomFunction_validator["inputNull"] is False and (not random_function or len(random_function) == 0):
                return Response({'OK': False, 'data': 'The Random function of the Challenge is missing!'},
                            status=status.HTTP_400_BAD_REQUEST)

            hard_function = data['hardFunction']

            if challenge_hardFunction_validator["inputNull"] is False and (not hard_function or len(hard_function) == 0):
                return Response({'OK': False, 'data': 'The Hard function of the Challenge is missing!'},
                            status=status.HTTP_400_BAD_REQUEST)

            language = data['language']

            if not language:
                return Response({'OK': False, 'data': 'Something went wrong on our side! We apologize!'},
                            status=status.HTTP_400_BAD_REQUEST)



            decoded_user_id = get_request_user_id(request)
            user = AppUser.objects.get(id=decoded_user_id)

            private = data['privateChallenge']

            with transaction.atomic():
                new_challenge = Challenge(time_limit=time_limit, private=private, title=title, description=description, author=user)
                new_challenge.save()
                new_code = Code(challenge=new_challenge, language=language, solution=true_function,
                                random_tests=random_function, hard_tests=hard_function)
                new_code.save()
        except Exception as e:
            return Response({'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'data': 'Success'}, status=status.HTTP_201_CREATED)





class GetChallenge(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        try:
            challenge = Challenge.objects.get(slug=slug)

            decoded_user_id = get_request_user_id(request)
            logged_in_user = AppUser.objects.get(id=decoded_user_id)


            if challenge.private:
                if challenge not in logged_in_user.authored_challenges.all():
                    found = False
                    for assignment in logged_in_user.assignments.all():
                        if challenge == assignment.challenge:
                            found = True
                    if not found:
                        return Response({"data": "This is a private challenge!"}, status=status.HTTP_403_FORBIDDEN)
            elif not challenge.public:
                if not logged_in_user.admin_user:
                    return Response({"data": "This challenge has not yet passed our verification!"}, status=status.HTTP_403_FORBIDDEN)

            serialized_challenge = ChallengeSerializer(challenge, context={'requesting_user': logged_in_user})
            return Response(serialized_challenge.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, slug):
        try:
            challenge = Challenge.objects.filter(slug=slug)[0]
            data = request.data
            title = data['title']
            language = data['language']
            description = data['description']
            true_function = data['trueFunction']
            random_function = data['randomFunction']
            hard_function = data['hardFunction']
            time_limit = data['timeLimit']
            private = data['private']


            challenge.title = title
            challenge.private = private
            challenge.description = description
            challenge.time_limit = time_limit

            code = None

            try:
                code = Code.objects.get(Q(challenge=challenge) & Q(language=language))
                code.random_tests = random_function
                code.solution = true_function
                code.hard_tests = hard_function
            except Exception as e:
                code = Code(challenge=challenge, solution=true_function, language=language,
                            random_tests=random_function, hard_tests=hard_function)
            finally:
                code.save()

            challenge.save()
            return Response({"data": 'Successfully modified!'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetChallenges(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, lower_limit, upper_limit):
        try:
            challenges = Challenge.objects.filter(Q(public=True) & Q(private=False)).order_by('-id')[lower_limit: upper_limit]
            print(challenges)

            serialized_challenge = ChallengeSerializer(challenges, many=True)
            return Response({"challenges": serialized_challenge.data, "length": len(Challenge.objects.all())}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetChallengesSearch(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, target_name):
        decoded_user_id = get_request_user_id(request)
        logged_in_user = AppUser.objects.get(id=decoded_user_id)


        challenges = Challenge.objects.filter(Q(slug__contains=slugify(target_name))).order_by('-id')
        challenges = challenges.filter((Q(private=True) & Q(author = logged_in_user)) | Q(private=False))

        if not len(challenges):
            return Response({'OK': False, 'data': 'Challenge not found!'},
                            status=status.HTTP_404_NOT_FOUND)
        serialized_challenges = ChallengeSerializer(challenges, many=True)
        return Response(serialized_challenges.data, status=status.HTTP_200_OK)


class AdminGetChallenges(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            decoded_user_id = get_request_user_id(request)
            logged_in_user = AppUser.objects.get(id=decoded_user_id)

            if not logged_in_user.admin_user:
                return Response({'data': 'Hey there now! You are not an admin!!'}, status=status.HTTP_403_FORBIDDEN)

            challenges = Challenge.objects.filter(Q(public=False) & Q(private=False) & Q(denied=False))
            return Response(ChallengeSerializer(challenges, many=True).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminGetDeniedChallenges(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            decoded_user_id = get_request_user_id(request)
            logged_in_user = AppUser.objects.get(id=decoded_user_id)
            if not logged_in_user.admin_user:
                return Response({'data': 'Hey there now! You are not an admin!!'}, status=status.HTTP_403_FORBIDDEN)

            challenges = Challenge.objects.filter(Q(public=False) & Q(private=False) & Q(denied=True))
            return Response(ChallengeSerializer(challenges, many=True).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class getChallengeStats(APIView):
    def get(self, request, slug):
        try:

            challenge = Challenge.objects.get(slug=slug)
            if not challenge:
                return Response({'data': 'No such challenge!'}, status=status.HTTP_404_NOT_FOUND)

            likes = Like.objects.filter(challenge=challenge)

            return Response({
                "data": {
                    "solved": challenge.solved,
                    "attempts": challenge.attempts,
                    "likes": len(likes)
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChallengeAdmin(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, slug):
        try:
            data = request.data
            verdict = data['verdict']


            challenge = Challenge.objects.get(slug=slug)
            decoded_user_id = get_request_user_id(request)
            logged_in_user = AppUser.objects.get(id=decoded_user_id)

            if not logged_in_user.admin_user:
                return Response({'data': 'Hey there now! You are not an admin!!'}, status=status.HTTP_403_FORBIDDEN)

            if verdict == 'difficulty':
                details = data['details']
                challenge.difficulty = details
                challenge.save()
                return Response({'data': 'Action completed admin!'}, status=status.HTTP_201_CREATED)


            if verdict == 'approve':
                challenge.public = True
            elif verdict == 'send-back':
                details = data['details']
                challenge.public = False
                challenge.status = 'Needs improvement'

                format_new_admin_email(challenge.author.username, challenge.title, details)
                send_email(receiver_email=challenge.author.email, message=new_admin_message)
            elif verdict == 'deny':
                challenge.public = False
                challenge.status = 'Denied'
                challenge.denied = True

            challenge.save()
            return Response({'data': 'Action completed admin!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

