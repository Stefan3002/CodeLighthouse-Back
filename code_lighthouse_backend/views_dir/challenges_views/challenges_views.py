from django.db import transaction
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from code_lighthouse_backend.models import Challenge, AppUser, Code, Reports
from code_lighthouse_backend.serializers import ChallengeSerializer
from code_lighthouse_backend.utils import get_request_user_id



class PostChallenge(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self):
        pass

    def post(self, request):
        try:
            data = request.data
            title = data['title']
            description = data['description']
            true_function = data['trueFunction']
            random_function = data['randomFunction']
            language = data['language']
            user_id = data['userId']
            private = data['privateChallenge']

            user = AppUser.objects.get(user_id=user_id)


            with transaction.atomic():
                new_challenge = Challenge(private=private, title=title, description=description, author=user)
                new_challenge.save()
                new_code = Code(challenge=new_challenge, language=language, solution=true_function,
                                random_tests=random_function)
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

            serialized_challenge = ChallengeSerializer(challenge)
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

            challenge.title = title
            challenge.description = description

            code = None

            try:
                code = Code.objects.get(Q(challenge=challenge) & Q(language=language))
                code.random_tests = random_function
                code.solution = true_function
            except Exception as e:
                code = Code(challenge=challenge, solution=true_function, language=language,
                            random_tests=random_function)
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
        challenges = Challenge.objects.all().order_by('-id')[lower_limit: upper_limit]
        serialized_challenge = ChallengeSerializer(challenges, many=True)
        return Response(serialized_challenge.data, status=status.HTTP_200_OK)


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


class ChallengeAdmin(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, slug):
        data = request.data
        verdict = data['verdict']

        try:
            challenge = Challenge.objects.get(slug=slug)
            decoded_user_id = get_request_user_id(request)
            logged_in_user = AppUser.objects.get(id=decoded_user_id)

            if not logged_in_user.admin_user:
                return Response({'data': 'Hey there now! You are not an admin!!'}, status=status.HTTP_403_FORBIDDEN)

            if verdict == 'approve':
                challenge.public = True
            elif verdict == 'send-back':
                challenge.public = False
                challenge.status = 'Needs improvement'
            elif verdict == 'deny':
                challenge.public = False
                challenge.status = 'Denied'
                challenge.denied = True

            challenge.save()
            return Response({'data': 'Action completed admin!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

