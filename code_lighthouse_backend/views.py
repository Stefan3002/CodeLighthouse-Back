import datetime
import os
import subprocess
import uuid
import docker
from django.db.models import Q

from rest_framework import serializers, status
from django.core.serializers import serialize
import json
from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import requires_csrf_token
from rest_framework.response import Response
from rest_framework.views import APIView

from code_lighthouse_backend.models import Challenge, AppUser, Lighthouse, Assignment, Like, Comment, Code
from code_lighthouse_backend.runUserCode import runPythonCode, runJavascriptCode
from code_lighthouse_backend.serializers import AppUserSerializer, LighthouseSerializer, ChallengeSerializer


# Create your views here.

class Auth(APIView):
    def get(self, request):
        token = get_token(request)
        data = {"aaa": "v"}
        response = HttpResponse(data, content_type='application/json')
        response.set_cookie('csrftoken', get_token(request))
        return response

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = AppUser.objects.filter(email=email)[0]
        if user.password == password:
            serialized_user = AppUserSerializer(user, context={'drill': True})
            return Response(serialized_user.data, status=status.HTTP_200_OK)
        else:
            return Response({'data': 'Wrong credentials!'}, status=status.HTTP_401_UNAUTHORIZED)


class RunUserCode(APIView):
    def post(self, request, slug):
        data = request.data
        language = data['language']
        if language == 'Python':
            try:
                logs_str = runPythonCode(request, slug)
            except Exception as e:
                return Response({'OK': False, 'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'OK': True, 'data': logs_str}, status=status.HTTP_200_OK)

        elif language == 'Javascript':
            try:
                logs_str = runJavascriptCode(request, slug)
                print(logs_str)
            except Exception as e:
                print(e)
                return Response({'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'data': logs_str}, status=status.HTTP_200_OK)


class CommentsView(APIView):
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
    def get(self, request):
        challenge = Challenge.objects.order_by('?')[0]
        serialized_challenge = serialize('json', [challenge])
        return HttpResponse(serialized_challenge, content_type='application/json')


class LikeView(APIView):
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
    def get(self, request, slug):
        try:
            challenge = Challenge.objects.filter(slug=slug)[0]
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

            code = Code.objects.get(Q(challenge=challenge) & Q(language=language))

            code.random_tests = random_function
            code.solution = true_function

            code.save()

            challenge.save()
            return Response({"data": 'Successfully modified!'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetLighthouse(APIView):
    def get(self, request, lighthouseID):
        lighthouse = Lighthouse.objects.filter(id=lighthouseID)[0]
        print(lighthouse)
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


class GetChallenges(APIView):
    def get(self, request, lower_limit, upper_limit):
        challenges = Challenge.objects.all().order_by('-id')[lower_limit: upper_limit]
        serialized_challenge = ChallengeSerializer(challenges, many=True)
        return Response(serialized_challenge.data, status=status.HTTP_200_OK)


class Assignments(APIView):
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


class GetLighthouses(APIView):
    def get(self, request, lower_limit, upper_limit):
        lighthouses = Lighthouse.objects.all()[lower_limit: upper_limit]
        serialized_lighthouses = LighthouseSerializer(lighthouses, many=True)
        return Response(serialized_lighthouses.data, status=status.HTTP_200_OK)


class PostChallenge(APIView):
    def get(self):
        pass

    def post(self, request):
        data = request.data
        title = data['title']
        description = data['description']
        trueFunction = data['trueFunction']
        randomFunction = data['randomFunction']

        new_challenge = Challenge(title=title, description=description, solution=trueFunction,
                                  random_tests=randomFunction)
        new_challenge.save()

        return Response({'data': 'Success'}, status=status.HTTP_201_CREATED)


class GetUser(APIView):
    def get(self, request, userID):
        user = AppUser.objects.filter(id=userID)[0]
        # print(user.lighthouses.all()[0])
        serialized_user = AppUserSerializer(user, context={'drill': True})
        return Response(serialized_user.data, status=status.HTTP_200_OK)


class CreateLighthouse(APIView):
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
