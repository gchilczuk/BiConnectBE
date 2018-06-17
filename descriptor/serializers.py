from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework import serializers, status
from rest_framework.exceptions import ParseError, NotFound, PermissionDenied

from .models import Person, Requirement, Meeting, Speech, Recommendation, Group, Category, BusinessDescription


class SimplePersonSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', required=True)
    last_name = serializers.CharField(source='user.last_name', required=True)
    username = serializers.CharField(source='user.username', required=False)
    email = serializers.CharField(source='user.email', required=False, allow_blank=True)

    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'username', 'email')

    def create(self, validated_data):
        user_data = validated_data.get('user')
        first_name = user_data.get('first_name')
        last_name = user_data.get('last_name')

        email = user_data.get('email', '')

        if email != '':
            email_taken = Person.objects.filter(user__email=email).count()
            if email_taken:
                raise ParseError("Email address is already used by another user!")

        group = validated_data['group']
        base_login = (first_name + last_name).lower()
        count_logins = Person.objects.filter(user__username__icontains=base_login).count()
        login = base_login + (str(count_logins) if count_logins > 0 else '')
        user = User.objects.create(first_name=first_name, last_name=last_name, email=email,
                                   username=login, password='')
        person = Person.objects.create(user=user, group=group, member=False)
        return person


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
                    raise NotFound("You are trying to update Requirement which does not exist"
                                   " or belongs to another speech!")
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
                    raise NotFound("You are trying to update Recommendation which does not exist"
                                   " or belongs to another speech!")
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


class BusinessDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessDescription
        fields = ('id', 'description')

    def update(self, instance, validated_data):
        if instance:
            instance.description = validated_data.get('description', '')
        else:
            instance = self.Meta.model.objects.create(**validated_data)
        instance.save()
        return instance


class SpeechSerializer(serializers.ModelSerializer):
    requirements = RequirementSerializer(many=True, read_only=True)
    recommendations = RecommendationSerializer(many=True, read_only=True)
    person = SimplePersonSerializer()
    business_description = BusinessDescriptionSerializer()
    confirmed = serializers.BooleanField(required=False)

    class Meta:
        model = Speech
        fields = ('id', 'requirements', 'recommendations', 'person', 'date',
                  'sound_file', 'business_description', 'confirmed')
        read_only_fields = ('id', 'date', 'confirmed')

    def save(self, speech):
        if speech.confirmed:
            raise PermissionDenied(detail="Confirmed speech cannot be modified", code=status.HTTP_423_LOCKED)
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
