from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from descriptor.models import Person
from descriptor.serializers import PersonSerializer


class HelloWorld(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        return Response({"text": "Hello world!"})


class PeopleView(ViewSet):
    queryset = Person.objects
    serializer_class = PersonSerializer

    def list(self, request):
        result = self.serializer_class(self.queryset.all(), many=True)
        return Response(result.data)

    def retrieve(self, request, pk=None):
        result = self.serializer_class(self.queryset.filter(pk=pk).first())
        return Response(result.data)
