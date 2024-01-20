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

from code_lighthouse_backend.email_sending.messages import new_announcement_message, format_new_announcement_email
from code_lighthouse_backend.email_sending.send_emails import send_email
from code_lighthouse_backend.models import Challenge, AppUser, Lighthouse, Assignment, Like, Comment, Code, Announcement
from code_lighthouse_backend.runUserCode import runPythonCode, runJavascriptCode, runRubyCode
from code_lighthouse_backend.serializers import AppUserSerializer, LighthouseSerializer, ChallengeSerializer, \
    SubmissionSerializer, AppUserPublicSerializer
from code_lighthouse_backend.utils import retrieve_token, retrieve_secret, get_request_user_id

import firebase_admin
from firebase_admin import credentials

from code_lighthouse_backend.validations.create_announcement_validation import announcement_content_validator



cred = credentials.Certificate(
    r"C:\Users\Stefan\PycharmProjects\djangoProject1\code_lighthouse_backend\codelighthouse-firebase-adminsdk-n38yt-961212f4bf.json")
# cred = credentials.Certificate(r"./codelighthouse-firebase-adminsdk-n38yt-961212f4bf.json")
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
        soft_time_limit = data['timeLimit']

        if language == 'Python':
            try:
                results = runPythonCode(request, slug, 'full', '', soft_time_limit)
                logs_str = results[0]
                exec_time = results[1]
                # Success!
                logs_str = format_logs_for_html(logs_str)
            except Exception as e:
                return handle_code_error(e)

            return Response({'OK': True, 'data': {'logs': logs_str, 'time': exec_time}}, status=status.HTTP_200_OK, content_type='text/plain')

        elif language == 'Javascript':
            try:
                logs_str = runJavascriptCode(request, slug, 'full', '')
                logs_str = format_logs_for_html(logs_str)
            except Exception as e:
                return handle_code_error(e)

            return Response({'data': logs_str}, status=status.HTTP_200_OK)

        elif language == 'Ruby':
            try:
                logs_str = runRubyCode(request, slug, 'full', '')
                logs_str = format_logs_for_html(logs_str)
            except Exception as e:
                return handle_code_error(e)

            return Response({'data': logs_str}, status=status.HTTP_200_OK)



class RunUserHardCode(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):

        # print(jwt.decode(token, 'django-insecure-op_4k4#z)fnvu%8jw01#o*n*3@@8)l*s7kiogd4i400f+qakw0', algorithms=["HS256"]))

        data = request.data
        language = data['language']
        # soft_time_limit = data['timeLimit']


        custom_hard_tests = data['hardTests']

        if language == 'Python':
            try:
                results = runPythonCode(request, slug, 'hard', custom_hard_tests)
                logs_str = results[0]
                exec_time = results[1]
                # Success!
                logs_str = format_logs_for_html(logs_str)
            except Exception as e:
                return handle_code_error(e)

            return Response({'OK': True, 'data': {'logs': logs_str, 'time': exec_time}}, status=status.HTTP_200_OK, content_type='text/plain')

        elif language == 'Javascript':
            try:
                logs_str = runJavascriptCode(request, slug, 'hard', custom_hard_tests)
                logs_str = format_logs_for_html(logs_str)
            except Exception as e:
                return handle_code_error(e)

            return Response({'data': logs_str}, status=status.HTTP_200_OK)

        elif language == 'Ruby':
            try:
                logs_str = runRubyCode(request, slug, 'hard', custom_hard_tests)
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


class Communities(APIView):
    def get(self, request):
        try:
            communities = Lighthouse.objects.filter(public=True)
            serialized_lighthouses = LighthouseSerializer(communities, many=True)
            return Response(serialized_lighthouses.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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


class Announcements(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            data = request.data
            lighthouse_id = data['lighthouseId']
            content = data['content']

            if announcement_content_validator["inputNull"] is False and (not content or len(content) == 0):
                return Response({'OK': False, 'data': 'Announcement is missing!'},
                            status=status.HTTP_400_BAD_REQUEST)

            if len(content) < announcement_content_validator["inputMin"]:
                return Response({'OK': False, 'data': 'Announcement is too short!'},
                            status=status.HTTP_400_BAD_REQUEST)


            decoded_user_id = get_request_user_id(request)
            logged_in_user = AppUser.objects.get(id=decoded_user_id)
            lighthouse = Lighthouse.objects.get(id=lighthouse_id)

            if not logged_in_user == lighthouse.author:
                return Response({"data": 'You are not the owner of this Lighthouse!'}, status=status.HTTP_403_FORBIDDEN)
            if len(content.strip()) < 15:
                return Response({"data": 'Too short announcement!'}, status=status.HTTP_400_BAD_REQUEST)

            new_announcement = Announcement(lighthouse=lighthouse, author=logged_in_user, content=content)
            new_announcement.save()

            # Send E-mails.
            # for receiver in lighthouse.people.all():
            #     format_new_announcement_email(receiver.username, lighthouse.name, content)
            #     send_email(receiver_email=receiver.email, message=new_announcement_message)

            return Response({"data": 'Successfully created!'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Assignments(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, lighthouseID):
        try:
            challenge_slug = request.data['selectedChallenge']
            due_date = request.data['dueDate']
            due_time = request.data['dueTime']
            users = request.data['users']

            lighthouse = Lighthouse.objects.get(id=lighthouseID)

            if lighthouse.archived:
                return Response({'data': 'This Lighthouse has been archived! It is Read - Only'}, status=status.HTTP_400_BAD_REQUEST)

            challenge = Challenge.objects.get(slug=challenge_slug)
            new_assignment = Assignment(due_date=due_date, due_time=due_time, challenge=challenge, lighthouse=lighthouse)

            new_assignment.save()

            for user_id in users:
                user = AppUser.objects.filter(user_id=user_id)[0]
                new_assignment.users.add(user)

            return Response({'data': 'Success!'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class GetUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, userID):
        try:
            decoded_user_id = get_request_user_id(request)

            if decoded_user_id == userID:
                user = AppUser.objects.filter(id=userID)[0]
                # print(user.lighthouses.all()[0])
                serialized_user = AppUserSerializer(user, context={'drill': True})
                return Response(serialized_user.data, status=status.HTTP_200_OK)
            else:
                user = AppUser.objects.filter(id=userID)[0]
                # Return the public info!
                serialized_user = AppUserPublicSerializer(user, context={'drill': True})
                return Response(serialized_user.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
