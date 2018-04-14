from django.urls import path, include
from rest_framework_extensions.routers import ExtendedSimpleRouter

from descriptor import views

router = ExtendedSimpleRouter(trailing_slash=False)
router.register(r'people', views.PeopleViewSet)
router.register(r'groups', views.GroupViewSet, base_name='group') \
    .register(r'meetings', views.MeetingViewSet,
              base_name='group-meeting', parents_query_lookups=['group'])

urlpatterns = [
    path('', include(router.urls)),
    path('hello/', views.HelloWorld.as_view()),
]
