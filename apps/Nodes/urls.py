from django.urls import re_path
from apps.Nodes.views import PersonList
from apps.Nodes.views import PhoneList
from apps.Nodes.views import MeetingPointList

urlpatterns = [
	re_path(r'^listPerson$', PersonList.as_view(), name='listPerson'),
	re_path(r'^listPhone$', PhoneList.as_view(), name='listPhone'),
	re_path(r'^listMeetingPoint$', MeetingPointList.as_view(), name='listMeetingPoint'),
]