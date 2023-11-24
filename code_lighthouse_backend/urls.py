from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from code_lighthouse_backend import views
from code_lighthouse_backend.views_dir.auth_views import auth_views
from code_lighthouse_backend.views_dir.lighthouse_views import lighthouse_views
from code_lighthouse_backend.views_dir.challenges_views import challenges_views
from code_lighthouse_backend.views_dir.reports_views import reports_views

urlpatterns = [
    path('token', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('run/<slug:slug>', views.RunUserCode.as_view()),
    path('auth/provider', auth_views.AuthProvider.as_view()),
    path('auth', auth_views.Auth.as_view()),
    path('random-challenge', views.RandomChallenge.as_view()),
    path('like/<slug:slug>', views.LikeView.as_view()),
    path('challenges', challenges_views.PostChallenge.as_view()),
    path('communities', views.Communities.as_view()),
    path('reports', reports_views.GetReports.as_view()),
    path('announcements', views.Announcements.as_view()),
    path('reports/<int:id>', reports_views.GetReports.as_view()),
    path('submissions/<int:assignment_id>', views.GetAssignmentSubmissionsView.as_view()),
    path('challenges/<slug:slug>/comments', views.CommentsView.as_view()),
    path('challenges/<slug:slug>', challenges_views.GetChallenge.as_view()),
    path('admin', challenges_views.AdminGetChallenges.as_view()),
    path('challenges-admin/<slug:slug>', challenges_views.ChallengeAdmin.as_view()),
    path('challenges-report/<slug:slug>', reports_views.ChallengeReport.as_view()),
    path('challenges/<int:lower_limit>/<int:upper_limit>', challenges_views.GetChallenges.as_view()),
    path('users/<int:userID>', views.GetUser.as_view()),
    path('lighthouses/<int:lighthouseID>', lighthouse_views.GetLighthouse.as_view()),
    path('assignments/<int:lighthouseID>', views.Assignments.as_view()),
    path('create-lighthouses', lighthouse_views.CreateLighthouse.as_view()),
    path('lighthouses/<int:lower_limit>/<int:upper_limit>', lighthouse_views.GetLighthouses.as_view())
]