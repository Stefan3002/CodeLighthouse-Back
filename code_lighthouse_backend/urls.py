from django.conf.urls.static import static
from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from code_lighthouse_backend import views
from code_lighthouse_backend.views_dir.announcements_views import announcements_views
from code_lighthouse_backend.views_dir.auth_views import auth_views
from code_lighthouse_backend.views_dir.enitities_views import entities_views, public_entities_views
from code_lighthouse_backend.views_dir.files_views import files_views
from code_lighthouse_backend.views_dir.lighthouse_views import lighthouse_views
from code_lighthouse_backend.views_dir.challenges_views import challenges_views
from code_lighthouse_backend.views_dir.reports_views import reports_views
from code_lighthouse_server import settings

urlpatterns = [
    # path('token', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('test', views.Test.as_view()),
    path('poll/<task_id>', views.TaskPoll.as_view()),

    path('run/<slug:slug>', views.RunUserCode.as_view()),
    path('run-hard/<slug:slug>', views.RunUserHardCode.as_view()),
    path('auth/provider', auth_views.AuthProvider.as_view()),
    path('auth', auth_views.Auth.as_view()),
    path('random-challenge', views.RandomChallenge.as_view()),
    path('like/<slug:slug>', views.LikeView.as_view()),

    path('public-entities', public_entities_views.PublicEntities.as_view()),
    path('reports', reports_views.GetReports.as_view()),
    path('announcements-delete/<int:announcement_id>', announcements_views.Announcements.as_view()),
    path('announcements', announcements_views.Announcements.as_view()),

    path('create-contest', views.Contests.as_view()),
    path('contests', views.GetContests.as_view()),
    path('contests/<int:id>', views.GetContest.as_view()),
    path('challenge-contest/<int:id>', views.ChallengeContest.as_view()),

    path('user-entity', entities_views.GetUserEntity.as_view()),

    path('check-captcha', views.Captcha.as_view()),
    path('check-captcha-log-in', views.CaptchaLogIn.as_view()),

    path('reports/<int:id>', reports_views.GetReports.as_view()),

    path('submissions/<int:assignment_id>', views.GetAssignmentSubmissionsView.as_view()),
    path('grade-submissions/<int:assignment_id>', views.GradeAssignmentSubmissionsView.as_view()),

    path('challenges/<slug:slug>/comments', views.CommentsView.as_view()),
    path('challenges/<slug:slug>', challenges_views.GetChallenge.as_view()),
    path('admin-denied', challenges_views.AdminGetDeniedChallenges.as_view()),
    path('admin', challenges_views.AdminGetChallenges.as_view()),
    path('chat-bot', views.ChatBot.as_view()),
    path('challenges-admin/<slug:slug>', challenges_views.ChallengeAdmin.as_view()),
    path('entity-report/<slug:slug>', reports_views.EntityReport.as_view()),
    path('challenges', challenges_views.GetChallenges.as_view()),
    path('challenges-search/<str:target_name>', challenges_views.GetChallengesSearch.as_view()),
    path('users/<int:userID>', views.GetUser.as_view()),
    path('notifications/<int:notification_id>', views.Notifications.as_view()),
    path('notifications-all', views.NotificationsAll.as_view()),
    path('logs', views.Logs.as_view()),

    path('challenge-stats/<slug:slug>', challenges_views.getChallengeStats.as_view()),

    path('contest-reset-password/<int:contestID>', views.ContestResetPassword.as_view()),
    path('contest-reset-email/<int:contestID>', views.ContestResetEmail.as_view()),
    path('contest-get-submissions/<int:contestID>', views.ContestSubmissions.as_view()),
    path('contest-participant-summary/<int:contestID>', views.ContestSummary.as_view()),
    path('contest-challenge-leaderboard/<int:contestID>/<slug:challengeSlug>', views.ContestChallengeLeaderboard.as_view()),

    path('purge-account',
         views.PurgeAccount.as_view()),

    path('file/<str:file_name>/<int:lighthouse_id>', files_views.ViewFile.as_view()),

    path('entities/<int:lighthouseID>', lighthouse_views.GetEntity.as_view()),
    path('lighthouses/<int:lighthouseID>', lighthouse_views.GetEntity.as_view()),
    path('lighthouses-enroll-change/<int:lighthouseID>', lighthouse_views.ChangeEnrollLighthouse.as_view()),
    path('content-preview', lighthouse_views.GetLighthousePreview.as_view()),

    path('assignments/<int:lighthouseID>', views.Assignments.as_view()),
    path('create-lighthouses', lighthouse_views.CreateLighthouse.as_view()),
    path('lighthouses/<int:lower_limit>/<int:upper_limit>', lighthouse_views.GetLighthouses.as_view())
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
