from django.urls import path, include
from rest_framework_extensions.routers import ExtendedSimpleRouter
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

from descriptor import views

router = ExtendedSimpleRouter(trailing_slash=False)
router.register(r'people', views.PeopleViewSet)
router.register(r'groups', views.GroupViewSet, base_name='group') \
    .register(r'meetings', views.MeetingViewSet,
              base_name='group-meeting', parents_query_lookups=['group']) \
    .register(r'speeches', views.SpeechViewSet,
              base_name='group-meeting-speech', parents_query_lookups=['group', 'meeting'])

urlpatterns = [
    path('auth', obtain_jwt_token),
    path('api-token-verify', verify_jwt_token),
    path('', include(router.urls)),
]
