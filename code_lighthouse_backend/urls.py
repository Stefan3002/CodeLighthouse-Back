from django.urls import path

from code_lighthouse_backend import views

urlpatterns = [
    path('run', views.RunUserCode.as_view()),
    path('auth', views.Auth.as_view()),
    path('auth', views.Auth.as_view()),
    path('random-challenge', views.RandomChallenge.as_view()),
    path('challenges', views.PostChallenge.as_view()),
    path('challenges/<slug:slug>', views.GetChallenge.as_view()),
    path('challenges/<int:lower_limit>/<int:upper_limit>', views.GetChallenges.as_view()),
    path('users/<int:userID>', views.GetUser.as_view())
]