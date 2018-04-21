from django.db import IntegrityError
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
    def update(self, instance, validated_data, **kwargs):
        print(kwargs.get('dupa', 'brak'))
        updated_ids = []
        for newreq in validated_data:
            updated_ids.append(newreq.get('id'))
            try:
                id = newreq.pop('id')
                req, created = Requirement.objects.get_or_create(id=id, speech_id=kwargs['speech_id'], defaults=newreq)
            except IntegrityError:
                raise Exception("Cwaniaczysz, wygląda to tak jakbyś próbował zmienić speech.")

            if not created:
                req.description = newreq['description']
                req.save()

        for req in instance:
            if req.id not in updated_ids:
                req.delete()


class RequirementSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    id = serializers.IntegerField()

    class Meta:
        model = Requirement
        fields = ('id', 'description', 'appearance_date', 'expiration_date',
                  'fulfilled_positively', 'categories')
        list_serializer_class = RequirementListSerializer


class RecommendationListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data, **kwargs):
        updated_ids = []
        for newrecom in validated_data:
            updated_ids.append(newrecom.get('id'))
            try:
                id = newrecom.pop('id')
                recom, created = Recommendation.objects.get_or_create(id=id, speech_id=kwargs['speech_id'],
                                                                      defaults=newrecom)
            except IntegrityError:
                raise Exception("Cwaniaczysz, wygląda to tak jakbyś próbował zmienić speech.")

            if not created:
                recom.description = newrecom['description']
                recom.save()

        for recom in instance:
            if recom.id not in updated_ids:
                recom.delete()


class RecommendationSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    id = serializers.IntegerField()

    class Meta:
        model = Recommendation
        fields = ('id', 'description', 'appearance_date', 'expiration_date', 'categories')
        list_serializer_class = RecommendationListSerializer


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
        speech.person = Person.objects.get(user__username=self.validated_data['person']['user']['username'])
        speech.save()
        return speech


class MeetingDetailSerializer(serializers.ModelSerializer):
    speeches = SpeechSerializer(many=True, read_only=True)

    class Meta:
        model = Meeting
        fields = ('id', 'date', 'count_members', 'count_guests', 'speeches')
        read_only_fields = ('speeches',)
