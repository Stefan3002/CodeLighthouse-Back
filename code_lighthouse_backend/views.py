import uuid

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

from code_lighthouse_backend.models import Challenge, AppUser, Lighthouse
from code_lighthouse_backend.serializers import AppUserSerializer, LighthouseSerializer


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
        if(user.password == password):
            serialized_user = AppUserSerializer(user, context={'drill': True})
            return Response(serialized_user.data, status=status.HTTP_200_OK)
        else:
            return Response({'data': 'Wrong credentials!'}, status=status.HTTP_401_UNAUTHORIZED)


class RunUserCode(APIView):
    def get(self, request):
        token = get_token(request)
        data = {"a": "v"}
        response = JsonResponse(data, status=200)
        response.set_cookie('csrftoken', get_token(request))
        return response

    def post(self, request):
        print('asdasdasd', request.POST)
        return Response({'asd': 'asd'}, status=status.HTTP_200_OK)



class RandomChallenge(View):
    def get(self, request):
        challenge = Challenge.objects.order_by('?')[0]
        print('asdasd', challenge)
        serialized_challenge = serialize('json', [challenge])
        return HttpResponse(serialized_challenge, content_type='application/json')


class GetChallenge(View):
    def get(self, request, slug):
        challenge = Challenge.objects.filter(slug=slug)
        serialized_challenge = serialize('json', challenge)
        return HttpResponse(serialized_challenge, content_type='application/json')


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

class GetChallenges(View):
    def get(self, request, lower_limit, upper_limit):
        challenges = Challenge.objects.all()[lower_limit : upper_limit]
        serialized_challenge = serialize('json', challenges, use_natural_foreign_keys=True)
        return HttpResponse(serialized_challenge, content_type='application/json')


class GetLighthouses(APIView):
    def get(self, request, lower_limit, upper_limit):
        lighthouses = Lighthouse.objects.all()[lower_limit : upper_limit]
        serialized_lighthouses = LighthouseSerializer(lighthouses, many=True)
        return Response(serialized_lighthouses.data, status=status.HTTP_200_OK)

class PostChallenge(View):
    def get(self):
        pass
    def post(self, request):
        print(request.POST)



class GetUser(APIView):
    def get(self, request, userID):
        user = AppUser.objects.filter(id=userID)[0]
        # print(user.lighthouses.all()[0])
        serialized_user = AppUserSerializer(user, context={'drill': True})
        return Response(serialized_user.data, status=status.HTTP_200_OK)