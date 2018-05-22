from django.urls import path, include
from rest_framework_extensions.routers import ExtendedSimpleRouter

from descriptor import views

router = ExtendedSimpleRouter(trailing_slash=False)
router.register(r'people', views.PeopleViewSet)
group = router.register(r'groups', views.GroupViewSet, base_name='group')
group.register(r'meetings', views.MeetingViewSet,
               base_name='group-meeting', parents_query_lookups=['group']) \
    .register(r'speeches', views.SpeechViewSet,
              base_name='group-meeting-speech', parents_query_lookups=['group', 'meeting'])

group.register(r'people', views.FastAddPersonViewSet,
               base_name='group-people', parents_query_lookups=['group'])

urlpatterns = [
    path('', include(router.urls)),
]
