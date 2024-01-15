from rest_framework import serializers

from code_lighthouse_backend.models import Lighthouse, AppUser, Challenge, Assignment, Comment, Like, Code, Submission, \
    Reports, Announcement


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['content', 'id', 'author']

    def get_author(self, comment):
        author = comment.author
        return AppUserSerializer(author).data


class ReportSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    assigned_admin = serializers.SerializerMethodField()
    challenge = serializers.SerializerMethodField()

    class Meta:
        model = Reports
        fields = '__all__'

    def get_author(self, report):
        author = report.author
        return AppUserSerializer(author).data

    def get_assigned_admin(self, report):
        admin = report.author
        return AppUserSerializer(admin).data

    def get_challenge(self, report):
        challenge = report.challenge
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


class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = '__all__'

    author = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    likes_received = serializers.SerializerMethodField()
    codes = serializers.SerializerMethodField()
    submissions = serializers.SerializerMethodField()

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

    def get_challenge(self, lighthouse):
        challenge = lighthouse.challenge
        return ChallengeSerializer(challenge).data

    def get_users(self, assignment):
        user_ids = assignment.users.all()
        return AppUserSerializer(user_ids, many=True).data


class LighthousePreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lighthouse
        fields = ['name', 'author', 'id']

    author = serializers.SerializerMethodField()

    def get_author(self, lighthouse):
        author = lighthouse.author
        return AppUserSerializer(author).data


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

class AppUserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['username', 'photoURL', 'score', 'solved_challenges']

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
