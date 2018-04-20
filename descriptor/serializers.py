from rest_framework import serializers

from .models import Person, Requirement, Meeting, Speech, Recommendation, Group, Category


class PersonPerfunctorySerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'username')

    def get(self):
        return Person.objects.get(user__username=self.username)


class PersonSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Person
        fields = ('id', 'first_name', 'last_name', 'email',
                  'username', 'member', 'group',
                  'newsletter', 'speech_confirm')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'city')


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ('id', 'date', 'count_members', 'count_guests')


class RequirementListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        print(instance)
        return instance


class RequirementSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    id = serializers.IntegerField()

    class Meta:
        model = Requirement
        fields = ('id', 'description', 'appearance_date', 'expiration_date',
                  'fulfilled_positively', 'categories')
        list_serializer_class = RequirementListSerializer


class RecommendationSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    id = serializers.IntegerField()

    class Meta:
        model = Recommendation
        fields = ('id', 'description', 'appearance_date', 'expiration_date', 'categories')


class SpeechSerializer(serializers.ModelSerializer):
    requirements = RequirementSerializer(many=True, read_only=True)
    recommendations = RecommendationSerializer(many=True, read_only=True)
    person = PersonPerfunctorySerializer()

    class Meta:
        model = Speech
        fields = ('id', 'requirements', 'recommendations', 'person', 'date', 'sound_file')
        read_only_fields = ('id', 'date')

    def save(self, pk):
        speech = self.Meta.model.objects.get(pk=pk)
        speech.date = self.validated_data['date']
        speech.person = self.validated_data['person'].get()
        speech.save()
        return speech


class MeetingDetailSerializer(serializers.ModelSerializer):
    speeches = SpeechSerializer(many=True, read_only=True)

    class Meta:
        model = Meeting
        fields = ('id', 'date', 'count_members', 'count_guests', 'speeches')
        read_only_fields = ('speeches',)
