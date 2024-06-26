import datetime

from django.db.models import Q
from rest_framework import serializers

import code_lighthouse_backend
from code_lighthouse_backend.models import Lighthouse, AppUser, Challenge, Assignment, Comment, Like, Code, Submission, \
    Reports, Announcement, Notification, Log, Contest


def serializeLogs(logs):
    most_time_logged_in = 0
    time_on_challenges = {}

    for log in logs:
        if log.type == 'auth':
            if log.time_out is not None:
                most_time_logged_in = max(most_time_logged_in, (log.time_out - log.time_in).total_seconds())

    for log in logs:
        if log.type == 'challenge':
            if log.challenge.id not in time_on_challenges:
                time_on_challenges[log.challenge.id] = 0
            if log.time_out is not None and log.time_in is not None:
                time_on_challenges[log.challenge.id] += ((log.time_out - log.time_in).total_seconds())

    # print("Most Time Logged In:", most_time_logged_in)
    # print("Time On Challenges:", time_on_challenges)

    return {
        "auth": most_time_logged_in,
        "challenges": time_on_challenges
    }


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['content', 'id', 'author', 'modified', 'slug']

    slug = serializers.SerializerMethodField()

    def get_author(self, comment):
        author = comment.author
        return AppUserSerializer(author).data

    def get_slug(self, comment):
        challenge_slug = comment.challenge.slug
        return challenge_slug


class ReportSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    # assigned_admin = serializers.SerializerMethodField()
    challenge = serializers.SerializerMethodField()

    class Meta:
        model = Reports
        fields = '__all__'

    def get_author(self, report):
        author = report.author
        return AppUserPublicSerializer(author).data

    def get_assigned_admin(self, report):
        admin = report.author
        return AppUserSerializer(admin).data

    def get_challenge(self, report):
        challenge = report.challenge
        if isinstance(challenge, code_lighthouse_backend.models.Comment):
            return CommentSerializer(challenge).data
        else:
            return ChallengeSerializer(challenge).data


class AnnouncementSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    lighthouse = serializers.SerializerMethodField()

    class Meta:
        model = Announcement
        fields = '__all__'

    def get_author(self, announcement):
        author = announcement.author
        return AppUserSerializer(author).data

    def get_lighthouse(self, announcement):
        lighthouse = announcement.lighthouse
        if self.context.get('drill'):
            return LighthouseSerializer(lighthouse).data
        else:
            return {}


class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = '__all__'


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'

    user = serializers.SerializerMethodField()
    challenge = serializers.SerializerMethodField()

    def get_challenge(self, submission):
        challenge = submission.challenge
        # if self.context.get('drill'):
        return challenge.slug
        # else:
        #     return {}

    def get_user(self, submission):
        user = submission.user
        return AppUserSerializer(user).data


class LogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'


class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = '__all__'

    author = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    likes_received = serializers.SerializerMethodField()
    codes = serializers.SerializerMethodField()
    submissions = serializers.SerializerMethodField()
    user_logs = serializers.SerializerMethodField()

    def get_user_logs(self, challenge):
        logs = Log.objects.filter(Q(challenge=challenge) & Q(author=self.context.get('requesting_user')))
        return serializeLogs(logs)

    def get_submissions(self, challenge):
        submissions = challenge.challenge_submissions.all()
        return SubmissionSerializer(submissions, many=True).data

    def get_codes(self, challenge):
        codes = challenge.codes
        return CodeSerializer(codes, many=True).data

    def get_likes_received(self, challenge):
        likes = challenge.likes_received
        return len(LikeSerializer(likes, many=True).data)

    def get_comments(self, challenge):
        comments = challenge.comments
        return CommentSerializer(comments, many=True).data

    def get_author(self, challenge):
        author = challenge.author
        return AppUserSerializer(author).data


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'

    users = serializers.SerializerMethodField()
    challenge = serializers.SerializerMethodField()
    lighthouse = serializers.SerializerMethodField()

    def get_challenge(self, lighthouse):
        challenge = lighthouse.challenge
        return ChallengeSerializer(challenge).data

    def get_users(self, assignment):
        user_ids = assignment.users.all()
        return AppUserSerializer(user_ids, many=True).data

    def get_lighthouse(self, assignment):
        lighthouse = assignment.lighthouse
        return LighthouseAssignmentSerializer(lighthouse).data


class LighthousePreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lighthouse
        fields = ['name', 'author', 'id']

    author = serializers.SerializerMethodField()

    def get_author(self, lighthouse):
        author = lighthouse.author
        return AppUserSerializer(author).data


class ContestPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ['name', 'author', 'id']

    author = serializers.SerializerMethodField()

    def get_author(self, contest):
        author = contest.author
        return AppUserSerializer(author).data


class LighthouseAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lighthouse
        fields = ['id', 'name', 'author']


class LighthouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lighthouse
        fields = '__all__'

    author = serializers.SerializerMethodField()
    people = serializers.SerializerMethodField()
    assignments = serializers.SerializerMethodField()
    announcements = serializers.SerializerMethodField()

    def get_announcements(self, lighthouse):
        announcements = lighthouse.announcements.all().order_by('id').reverse()
        return AnnouncementSerializer(announcements, many=True).data

    def get_assignments(self, lighthouse):
        assignments = Assignment.objects.filter(lighthouse=lighthouse)
        return AssignmentSerializer(assignments, many=True).data

    def get_people(self, lighthouse):
        people = lighthouse.people.all()
        return AppUserSerializer(people, many=True).data

    def get_author(self, lighthouse):
        author = lighthouse.author
        return AppUserSerializer(author).data

    # people = serializers.StringRelatedField(many=True)  # Serialize people as a list of strings (usernames)


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = '__all__'

    challenges = serializers.SerializerMethodField()
    people = serializers.SerializerMethodField()

    def get_challenges(self, contest):
        challenges = contest.challenges.all()
        return ChallengeSerializer(challenges, many=True).data

    def get_people(self, contest):
        people = contest.people.all()
        return AppUserSerializer(people, many=True).data


class AppUserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['username', 'photoURL', 'score', 'solved_challenges']

    solved_challenges = serializers.SerializerMethodField()

    def get_solved_challenges(self, app_user):
        challenges = app_user.solved_challenges.all()
        if self.context.get('drill'):
            return ChallengeSerializer(challenges, many=True).data
        else:
            return {}


class AppUserSerializer(serializers.ModelSerializer):
    enrolled_lighthouses = serializers.SerializerMethodField()
    authored_challenges = serializers.SerializerMethodField()
    solved_challenges = serializers.SerializerMethodField()
    liked_challenges = serializers.SerializerMethodField()
    submissions = serializers.SerializerMethodField()
    assigned_reports = serializers.SerializerMethodField()
    notifications = serializers.SerializerMethodField()
    logs = serializers.SerializerMethodField()

    def get_logs(self, app_user):
        logs = Log.objects.filter(author=app_user)
        return serializeLogs(logs)

    def get_solved_challenges(self, app_user):
        challenges = app_user.solved_challenges.all()
        if self.context.get('drill'):
            return ChallengeSerializer(challenges, many=True).data
        else:
            return {}

    def get_submissions(self, app_user):
        submissions = app_user.submissions.all()
        if self.context.get('drill'):
            return SubmissionSerializer(submissions, many=True).data
        else:
            return {}

    def get_assigned_reports(self, app_user):
        reports = app_user.assigned_reports.all()
        if self.context.get('drill'):
            return ReportSerializer(reports, many=True).data
        else:
            return {}

    def get_liked_challenges(self, app_user):
        liked_challenges = app_user.liked_challenges
        return LikeSerializer(liked_challenges, many=True).data

    def get_notifications(self, app_user):
        notifications = app_user.notifications.all()
        return NotificationSerializer(notifications, many=True).data

    def get_authored_challenges(self, app_user):
        challenges = app_user.authored_challenges.all()
        if self.context.get('drill'):
            return ChallengeSerializer(challenges, many=True).data
        else:
            return {}

    def get_enrolled_lighthouses(self, app_user):
        lighthouses = app_user.enrolled_Lighthouses.all()
        if self.context.get('drill'):
            return LighthouseSerializer(lighthouses, many=True).data
        else:
            return {}

    # lighthouses = LighthouseSerializer(many=True, read_only=True, source='lighthouses.all')
    class Meta:
        model = AppUser
        exclude = ['password', 'email']
