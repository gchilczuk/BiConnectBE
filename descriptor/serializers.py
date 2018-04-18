from rest_framework import serializers

from .models import Person, Requirement, Meeting, Speech, Recommendation, Group


class PersonSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'email',
                  'username', 'member', 'group',
                  'newsletter', 'speech_confirm')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'city')


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ('id', 'date', 'count_members', 'count_guests')


class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = ('description', 'appearance_date', 'expiration_date',
                  'fulfilled_positively', 'categories')


class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = ('description', 'appearance_date', 'expiration_date', 'categories')


class SpeechSerializer(serializers.ModelSerializer):
    requirements = RequirementSerializer(many=True, read_only=True)
    recommendations = RecommendationSerializer(many=True, read_only=True)
    person = PersonSerializer()

    class Meta:
        model = Speech
        fields = ('id', 'requirements', 'recommendations', 'person', 'date', 'sound_file')


class MeetingDetailSerializer(serializers.ModelSerializer):
    speeches = SpeechSerializer(many=True, read_only=True)

    class Meta:
        model = Meeting
        fields = ('id', 'date', 'count_members', 'count_guests', 'speeches')
        read_only_fields = ('speeches',)
