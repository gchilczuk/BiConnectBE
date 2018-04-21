from django.http import HttpResponse
from django.utils.encoding import smart_str
from rest_framework import permissions
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework_extensions.mixins import DetailSerializerMixin
from rest_framework.decorators import action

from descriptor.models import Person, Meeting, Group
from descriptor.serializers import PersonSerializer, MeetingSerializer, GroupSerializer, MeetingDetailSerializer
from descriptor.utils import Note


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
