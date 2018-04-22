from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ParseError, NotFound

from .models import Person, Requirement, Meeting, Speech, Recommendation, Group, Category


class SimplePersonSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'username')


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
        updated_ids = []
        for newreq in validated_data:
            id = newreq.pop('id', None)

            if id is None:
                req = Requirement.objects.create(speech_id=kwargs['speech_id'], **newreq)
                updated_ids.append(req.id)
                req.save()

            else:
                try:
                    req = instance.get(id=id, speech_id=kwargs['speech_id'])

                except IntegrityError:
                    raise ParseError("You cannot reassign Requirement to another speech.")
                except Requirement.DoesNotExist:
                    raise NotFound("You are trying to update Requiremnt which does not exist!")
                updated_ids.append(id)
                req.description = newreq['description']
                req.save()

        for req in instance:
            if req.id not in updated_ids:
                req.delete()


class RequirementSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Requirement
        fields = ('id', 'description', 'appearance_date', 'expiration_date',
                  'fulfilled_positively', 'categories')
        list_serializer_class = RequirementListSerializer


class RecommendationListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data, **kwargs):
        updated_ids = []
        for newrecom in validated_data:
            id = newrecom.pop('id', None)

            if id is None:
                recom = instance.create(speech_id=kwargs['speech_id'], **newrecom)
                updated_ids.append(recom.id)
                recom.save()

            else:
                try:
                    recom = instance.get(id=id, speech_id=kwargs['speech_id'])
                except IntegrityError:
                    raise ParseError("You cannot reassign Recommendation to another speech.")
                except Recommendation.DoesNotExist:
                    raise NotFound("You are trying to update Recommendation which does not exist!")
                updated_ids.append(id)
                recom.description = newrecom['description']
                recom.save()

        for recom in instance:
            if recom.id not in updated_ids:
                recom.delete()


class RecommendationSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Recommendation
        fields = ('id', 'description', 'appearance_date', 'expiration_date', 'categories')
        list_serializer_class = RecommendationListSerializer


class SpeechSerializer(serializers.ModelSerializer):
    requirements = RequirementSerializer(many=True, read_only=True)
    recommendations = RecommendationSerializer(many=True, read_only=True)
    person = SimplePersonSerializer()

    class Meta:
        model = Speech
        fields = ('id', 'requirements', 'recommendations', 'person', 'date', 'sound_file')
        read_only_fields = ('id', 'date')

    def save(self, pk):
        speech = self.Meta.model.objects.get(pk=pk)
        try:
            speech.person = Person.objects.get(user__username=self.validated_data['person']['user']['username'])
        except Person.DoesNotExist:
            raise NotFound("There is no Person with given username")
        speech.save()
        return speech


class MeetingDetailSerializer(serializers.ModelSerializer):
    speeches = SpeechSerializer(many=True, read_only=True)

    class Meta:
        model = Meeting
        fields = ('id', 'date', 'count_members', 'count_guests', 'speeches')
        read_only_fields = ('speeches',)
