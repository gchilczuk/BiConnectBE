from django.db import transaction
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework_extensions.mixins import DetailSerializerMixin

from descriptor.models import Person, Meeting, Group, Speech, Requirement, Recommendation, BusinessDescription
from descriptor.serializers import PersonSerializer, MeetingSerializer, GroupSerializer, MeetingDetailSerializer, \
    SpeechSerializer, RequirementSerializer, RecommendationSerializer, SimplePersonSerializer, \
    BusinessDescriptionSerializer
from descriptor.utils import Note


class PeopleViewSet(ViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Person.objects
    serializer_class = PersonSerializer

    def list(self, request):
        result = self.serializer_class(self.queryset.all(), many=True)
        return Response(result.data)

    def retrieve(self, request, pk=None):
        result = self.serializer_class(self.queryset.filter(pk=pk).first())
        return Response(result.data)


class FastAddPersonViewSet(ViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Person.objects
    serializer_class = SimplePersonSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data.copy()
        data['group'] = Group.objects.get(id=self.kwargs['parent_lookup_group'])
        result = serializer.create(data)

        return Response(self.serializer_class(result).data)


class GroupViewSet(ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Group.objects
    serializer_class = GroupSerializer


class MeetingViewSet(DetailSerializerMixin, ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MeetingSerializer
    serializer_detail_class = MeetingDetailSerializer

    def get_queryset(self, *args, **kwargs):
        for m in Meeting.objects.all(): m.save()
        return Meeting.objects.filter(group=self.kwargs['parent_lookup_group'])

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            meeting = self.get_queryset().create(**serializer.validated_data,
                                                 group_id=self.kwargs['parent_lookup_group'])
            return Response(self.serializer_class(meeting).data)

    @action(detail=True)
    def note(self, request, **kwargs):
        try:
            meeting = self.get_queryset().get(pk=kwargs.get('pk'))
        except Meeting.DoesNotExist:
            raise NotFound('There is no meeting with such id in this group')
        note = Note(meeting)
        file_path = note.generate_txt()
        response = HttpResponse(open(file_path, 'rb').read(), content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename="notatka.txt"'
        return response


class SpeechViewSet(ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SpeechSerializer

    def get_queryset(self, *args, **kwargs):
        return Speech.objects.filter(meeting_id=self.kwargs['parent_lookup_meeting'])

    def create(self, request, *args, **kwargs):
        speech = self.get_queryset().create(meeting_id=self.kwargs['parent_lookup_meeting'])
        speech.meeting.save()
        return Response(self.serializer_class(speech).data)

    def update(self, request, *args, **kwargs):
        speech_id = kwargs.get('pk')
        speech = Speech.objects.get(pk=speech_id)
        serializer = self.serializer_class(data=request.data)
        serializer_req = RequirementSerializer(data=request.data.get('requirements'), many=True)
        serializer_rec = RecommendationSerializer(data=request.data.get('recommendations'), many=True)
        serializer_desc = BusinessDescriptionSerializer(data=request.data.get('business_description'))

        if (serializer.is_valid(raise_exception=True)
                and serializer_rec.is_valid(raise_exception=True)
                and serializer_req.is_valid(raise_exception=True)
                and serializer_desc.is_valid(raise_exception=True)):
            with transaction.atomic():
                try:
                    serializer.save(speech_id)
                except Speech.DoesNotExist:
                    raise NotFound("No such speech")

                requirements = Requirement.objects.filter(speech_id=speech_id)
                recommendations = Recommendation.objects.filter(speech_id=speech_id)
                business_description = speech.business_description

                serializer_req.update(requirements, serializer_req.validated_data, speech_id=speech_id)
                serializer_rec.update(recommendations, serializer_rec.validated_data, speech_id=speech_id)
                bdesc = serializer_desc.update(business_description, serializer_desc.validated_data)

                if business_description is None:
                    speech.business_description = bdesc
                speech.save()


        speech.meeting.save()
        return Response(self.serializer_class(speech).data)
