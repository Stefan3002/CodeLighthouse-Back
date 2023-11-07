from django.urls import path

from code_lighthouse_backend import views

urlpatterns = [
    path('run/<slug:slug>', views.RunUserCode.as_view()),
    path('auth', views.Auth.as_view()),
    path('random-challenge', views.RandomChallenge.as_view()),
    path('like/<slug:slug>', views.LikeView.as_view()),
    path('challenges', views.PostChallenge.as_view()),
    path('submissions/<int:assignment_id>', views.GetAssignmentSubmissionsView.as_view()),
    path('challenges/<slug:slug>/comments', views.CommentsView.as_view()),
    path('challenges/<slug:slug>', views.GetChallenge.as_view()),
    path('challenges/<int:lower_limit>/<int:upper_limit>', views.GetChallenges.as_view()),
    path('users/<int:userID>', views.GetUser.as_view()),
    path('lighthouses/<int:lighthouseID>', views.GetLighthouse.as_view()),
    path('assignments/<int:lighthouseID>', views.Assignments.as_view()),
    path('create-lighthouses', views.CreateLighthouse.as_view()),
    path('lighthouses/<int:lower_limit>/<int:upper_limit>', views.GetLighthouses.as_view())
]