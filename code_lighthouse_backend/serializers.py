from rest_framework import serializers

from code_lighthouse_backend.models import Lighthouse, AppUser, Challenge


class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = '__all__'

    author = serializers.SerializerMethodField()
    def get_author(self, challenge):
        author = challenge.author
        return AppUserSerializer(author).data
class LighthouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lighthouse
        fields = '__all__'

    author = serializers.SerializerMethodField()
    people = serializers.SerializerMethodField()

    def get_people(self, lighthouse):
        people = lighthouse.people.all()
        return AppUserSerializer(people, many=True).data
    def get_author(self, lighthouse):
        author = lighthouse.author
        return AppUserSerializer(author).data

    # people = serializers.StringRelatedField(many=True)  # Serialize people as a list of strings (usernames)
class AppUserSerializer(serializers.ModelSerializer):
    enrolled_lighthouses = serializers.SerializerMethodField()

    def get_enrolled_lighthouses(self, app_user):
        lighthouses = app_user.enrolled_Lighthouses.all()
        if self.context.get('drill'):
            return LighthouseSerializer(lighthouses, many=True).data
        else:
            return {}

    # lighthouses = LighthouseSerializer(many=True, read_only=True, source='lighthouses.all')
    class Meta:
        model = AppUser
        # depth = 2
        fields = '__all__'