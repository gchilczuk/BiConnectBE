from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework_extensions.mixins import DetailSerializerMixin

from descriptor.models import Person, Meeting, Group, Speech, Requirement
from descriptor.serializers import PersonSerializer, MeetingSerializer, GroupSerializer, MeetingDetailSerializer, \
    SpeechSerializer, RequirementSerializer, RecommendationSerializer


class HelloWorld(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        return Response({"text": "Hello world!"})


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


class GroupViewSet(ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Group.objects
    serializer_class = GroupSerializer


class MeetingViewSet(DetailSerializerMixin, ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MeetingSerializer
    serializer_detail_class = MeetingDetailSerializer

    def get_queryset(self, *args, **kwargs):
        return Meeting.objects.filter(group=self.kwargs['parent_lookup_group'])

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            meeting = self.get_queryset().create(**serializer.validated_data,
                                                 group_id=self.kwargs['parent_lookup_group'])
            return Response(self.serializer_class(meeting).data)


class SpeechViewSet(ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SpeechSerializer

    def get_queryset(self, *args, **kwargs):
        return Speech.objects.filter(meeting_id=self.kwargs['parent_lookup_meeting'])

    def create(self, request, *args, **kwargs):
        speech = self.get_queryset().create(meeting_id=self.kwargs['parent_lookup_meeting'])
        return Response(self.serializer_class(speech).data)

    def update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        serializer = self.serializer_class(data=request.data)
        serializer_req = RequirementSerializer(Requirement.objects.filter(speech_id=kwargs.get('pk')), data=request.data.get('requirements'), many=True)
        serializer_rec = RecommendationSerializer(data=request.data.get('recommendations'), many=True)


        if (serializer.is_valid(raise_exception=True)
                and serializer_rec.is_valid(raise_exception=True)
                and serializer_req.is_valid(raise_exception=True)):
            serializer_req.save()

            # speech = serializer.save(kwargs.get('pk'))

            # rec = speech.recommendations.all()
            # req = speech.requirements.all()

            # return Response(self.serializer_class(speech).data)

        return HttpResponse("Elo")
