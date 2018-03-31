from django.shortcuts import render
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView


class HelloWorld(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        return Response({"text": "Hello world!"})
