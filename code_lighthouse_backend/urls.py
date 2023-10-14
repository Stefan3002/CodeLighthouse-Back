from django.urls import path

from code_lighthouse_backend import views

urlpatterns = [
    path('run', views.RunUserCode.as_view()),
    path('auth', views.Auth.as_view()),
    path('random-challenge', views.RandomChallenge.as_view())
]