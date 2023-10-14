from django.core.serializers import serialize
import json
from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.views import View

from code_lighthouse_backend.models import Challenge


# Create your views here.

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


class Auth(View):
    def post(self, request):
        print(request.POST)


class RandomChallenge(View):
    def get(self, request):
        challenge = Challenge.objects.order_by('?')[0]
        serialized_challenge = serialize('json', [challenge])
        return HttpResponse(serialized_challenge, content_type='application/json')
