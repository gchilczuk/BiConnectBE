from django.urls import path

from descriptor.views import HelloWorld

urlpatterns = [
    path('hello/', HelloWorld.as_view())
]
