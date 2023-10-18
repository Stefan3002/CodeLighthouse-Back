from django.core.serializers import serialize
import json
from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import requires_csrf_token

from code_lighthouse_backend.models import Challenge, AppUser


# Create your views here.

class Auth(View):
    def get(self, request):
        token = get_token(request)
        data = {"aaa": "v"}
        response = HttpResponse(data, content_type='application/json')
        response.set_cookie('csrftoken', get_token(request))
        return response


class RunUserCode(View):
    def get(self, request):
        token = get_token(request)
        data = {"a": "v"}
        response = JsonResponse(data, status=200)
        response.set_cookie('csrftoken', get_token(request))
        return response

    def post(self, request):
        print('asdasdasd', request.POST)
        return JsonResponse({}, status=200)



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


class GetChallenges(View):
    def get(self, request, lower_limit, upper_limit):
        challenges = Challenge.objects.all()[lower_limit : upper_limit]
        serialized_challenge = serialize('json', challenges, use_natural_foreign_keys=True)
        return HttpResponse(serialized_challenge, content_type='application/json')

class PostChallenge(View):
    def get(self):
        pass
    def post(self, request):
        print(request.POST)


class GetUser(View):
    def get(self, request, userID):
        user = AppUser.objects.filter(id=userID)[0]
        serialized_user = serialize('json', [user])
        return HttpResponse(serialized_user, content_type='application/json')