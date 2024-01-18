import sys
import traceback

import firebase_admin
import jwt
from django.db import transaction
from django.db.models import Q
from firebase_admin import auth
from rest_framework import status
from django.core.serializers import serialize
from django.http import HttpResponse
from django.views import View
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from code_lighthouse_backend.models import Challenge, AppUser, Lighthouse, Assignment, Like, Comment, Code, Reports
from code_lighthouse_backend.runUserCode import runPythonCode, runJavascriptCode, runRubyCode
from code_lighthouse_backend.serializers import AppUserSerializer, LighthouseSerializer, ChallengeSerializer, \
    SubmissionSerializer, ReportSerializer
from code_lighthouse_backend.utils import retrieve_token, retrieve_secret, get_request_user_id

import firebase_admin
from firebase_admin import credentials


class GetReports(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        try:
            report = Reports.objects.get(id=id)
            admin = report.assigned_admin

            decoded_user_id = get_request_user_id(request)
            logged_in_user = AppUser.objects.get(id=decoded_user_id)

            if logged_in_user != admin:
                return Response({'data': 'This report has not been assigned to you admin!'}, status=status.HTTP_403_FORBIDDEN)

            report.closed = True
            report.save()

            return Response({'data': 'Report successfully closed!'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def get(self, request):
        try:
            decoded_user_id = get_request_user_id(request)
            logged_in_user = AppUser.objects.get(id=decoded_user_id)

            reports = Reports.objects.filter(Q(closed=False))

            return Response(ReportSerializer(reports, many=True).data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



def load_balance_report_admins():
    admins = list(AppUser.objects.filter(admin_user=True))
    print(admins.sort(key=lambda user: len(user.reports_admined.all())))
    print(admins)

    return admins[0]



class ChallengeReport(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, slug):
        try:
            data = request.data
            reason = data['reason']
            comment = None

            if reason == 'description':
                comment = data['comments']
                read_code_of_conduct = data['readCodeofConduct']
                if not read_code_of_conduct:
                    return Response({'data': 'You must read the Code of Conduct'}, status=status.HTTP_403_FORBIDDEN)
                if not comment or len(comment.strip()) == 0:
                    return Response({'data': 'You must explain why you reported this challenge.'}, status=status.HTTP_400_BAD_REQUEST)
                if len(comment.strip()) < 15:
                    return Response({'data': 'Please be more explicit when saying why reported this challenge!'}, status=status.HTTP_400_BAD_REQUEST)
                if len(comment.strip()) > 1000:
                    return Response({'data': 'Please shorten your reason for reporting the challenge.'}, status=status.HTTP_400_BAD_REQUEST)

            challenge = Challenge.objects.get(slug=slug)
            decoded_user_id = get_request_user_id(request)
            logged_in_user = AppUser.objects.get(id=decoded_user_id)

            if Reports.objects.filter(Q(author=logged_in_user) & Q(reason=reason)):
                return Response({'data': 'You can only report this challenge for this reason once.'},
                                status=status.HTTP_403_FORBIDDEN)

            assigned_admin = load_balance_report_admins()


            new_report = Reports(author=logged_in_user, comment=comment, reason=reason, assigned_admin=assigned_admin, challenge=challenge)

            new_report.save()
            return Response({'data': 'Report has been submitted and already assigned to an admin.'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)