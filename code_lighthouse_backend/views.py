import sys
import traceback

import firebase_admin
import jwt
from django.db import transaction
from django.db.models import Q
from firebase_admin import auth
from rest_framework import status
from django.core.serializers import serialize
from django.http import HttpResponse
from django.views import View
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from code_lighthouse_backend.models import Challenge, AppUser, Lighthouse, Assignment, Like, Comment, Code
from code_lighthouse_backend.runUserCode import runPythonCode, runJavascriptCode, runRubyCode
from code_lighthouse_backend.serializers import AppUserSerializer, LighthouseSerializer, ChallengeSerializer, \
    SubmissionSerializer
from code_lighthouse_backend.utils import retrieve_token, retrieve_secret, get_request_user_id




import firebase_admin
from firebase_admin import credentials



cred = credentials.Certificate(r"C:\Users\Stefan\PycharmProjects\djangoProject1\code_lighthouse_backend\codelighthouse-firebase-adminsdk-n38yt-961212f4bf.json")
firebase_admin.initialize_app(cred)



def format_logs_for_html(logs):
    html_logs = '<p>' + logs.replace('\n', '</p><p>')
    html_logs = html_logs.replace('\t', '&nbsp;&nbsp;')
    return html_logs
def handle_code_error(e):
    error_str = format_logs_for_html(str(e))
    return Response({'OK': False, 'data': error_str}, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content_type='text/plain')

class RunUserCode(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, slug):

        # print(jwt.decode(token, 'django-insecure-op_4k4#z)fnvu%8jw01#o*n*3@@8)l*s7kiogd4i400f+qakw0', algorithms=["HS256"]))

        data = request.data
        language = data['language']

        if language == 'Python':
            try:
                logs_str = runPythonCode(request, slug)
                # Success!
                logs_str = format_logs_for_html(logs_str)
            except Exception as e:
                return handle_code_error(e)

            return Response({'OK': True, 'data': logs_str}, status=status.HTTP_200_OK, content_type='text/plain')

        elif language == 'Javascript':
            try:
                logs_str = runJavascriptCode(request, slug)
                logs_str = format_logs_for_html(logs_str)
            except Exception as e:
                return handle_code_error(e)

            return Response({'data': logs_str}, status=status.HTTP_200_OK)

        elif language == 'Ruby':
            try:
                logs_str = runRubyCode(request, slug)
                logs_str = format_logs_for_html(logs_str)
            except Exception as e:
                return handle_code_error(e)

            return Response({'data': logs_str}, status=status.HTTP_200_OK)


class GetAssignmentSubmissionsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, assignment_id):
        try:
            assignment = Assignment.objects.get(id=assignment_id)

            challenge = assignment.challenge
            submissions = challenge.challenge_submissions.all().order_by('user')
            users = assignment.users.all().order_by('username')

            returned_submissions = {}

            for submission in submissions:
                if submission.user in users:
                    username = submission.user.username
                    data = (returned_submissions.get(username, []))
                    data.append(SubmissionSerializer(submission).data)
                    returned_submissions[username] = data

            return Response(returned_submissions, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, slug):
        try:
            data = request.data
            user_id = request.data['userId']
            content = request.data['content']
            challenge = Challenge.objects.get(slug=slug)
            user = AppUser.objects.get(user_id=user_id)
            new_comment = Comment(content=content, author=user, challenge=challenge)
            print(new_comment)
            new_comment.save()
            return Response({"data": 'Successfully saved!'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RandomChallenge(View):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        challenge = Challenge.objects.order_by('?')[0]
        serialized_challenge = serialize('json', [challenge])
        return HttpResponse(serialized_challenge, content_type='application/json')


class LikeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, slug):
        try:
            user_id = request.data['userId']
            user = AppUser.objects.filter(user_id=user_id)[0]
            challenge = Challenge.objects.filter(slug=slug)[0]

            like = Like.objects.filter(user=user, challenge=challenge)
            if not like:
                newLike = Like(challenge=challenge, user=user)
                newLike.save()
            else:
                like.delete()
            return Response({"data": 'Successfully saved!'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetChallenge(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, slug):
        try:
            challenge = Challenge.objects.get(slug=slug)
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


class Assignments(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, lighthouseID):
        challenge_slug = request.data['selectedChallenge']
        due_date = request.data['dueDate']
        due_time = request.data['dueTime']
        users = request.data['users']
        lighthouse = Lighthouse.objects.filter(id=lighthouseID)[0]
        challenge = Challenge.objects.filter(slug=challenge_slug)[0]
        new_assignment = Assignment(due_date=due_date, due_time=due_time, challenge=challenge, lighthouse=lighthouse)

        new_assignment.save()

        for user_id in users:
            user = AppUser.objects.filter(user_id=user_id)[0]
            new_assignment.users.add(user)

        return Response({'data': 'Success!'}, status=status.HTTP_201_CREATED)




class PostChallenge(APIView):
    def get(self):
        pass

    def post(self, request):
        data = request.data
        title = data['title']
        description = data['description']
        true_function = data['trueFunction']
        random_function = data['randomFunction']
        language = data['language']
        user_id = data['userId']
        user = AppUser.objects.get(user_id=user_id)

        try:
            with transaction.atomic():
                new_challenge = Challenge(title=title, description=description, author=user)
                new_challenge.save()
                new_code = Code(challenge=new_challenge, language=language, solution=true_function,
                                random_tests=random_function)
                new_code.save()
        except Exception as e:
            return Response({'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'data': 'Success'}, status=status.HTTP_201_CREATED)


class GetUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, userID):

        decoded_user_id = get_request_user_id(request)

        if decoded_user_id == userID:
            user = AppUser.objects.filter(id=userID)[0]
            # print(user.lighthouses.all()[0])
            serialized_user = AppUserSerializer(user, context={'drill': True})
            return Response(serialized_user.data, status=status.HTTP_200_OK)
        else:
            return Response({'data': 'Forbidden info!'}, status=status.HTTP_403_FORBIDDEN)



