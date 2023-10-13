from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.views import View


# Create your views here.

class RunUserCode(View):
    def get(self, request):
        token = get_token(request)
        data =  {"a": "v"}
        response = JsonResponse(data, status=200)
        response.set_cookie('csrftoken', get_token(request))
        return response

    def post(self, request):
        print('asdasdasd', request.POST)
        return JsonResponse({}, status=200)

class Auth(View):
    def post(self, request):
        print(request.POST)
