from django.urls import path, include
from rest_framework import routers

from descriptor import views

router = routers.DefaultRouter()
router.register('people', views.PeopleView)

urlpatterns = [
    path('api/', include(router.urls)),
    path('hello/', views.HelloWorld.as_view()),
]
