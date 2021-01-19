from django.urls import re_path
from apps.Nodes.views import PersonList, PersonCreate
from apps.Nodes.views import PhoneList, PhoneCreate
from apps.Nodes.views import MeetingPointList, MeetingPointCreate

urlpatterns = [
	re_path(r'^newPerson$', PersonCreate.as_view(), name='newPerson'),
	re_path(r'^newPhone$', PhoneCreate.as_view(), name='newPhone'),
	re_path(r'^newMeetingPoint$', MeetingPointCreate.as_view(), name='newMeetingPoint'),
	re_path(r'^listPerson$', PersonList.as_view(), name='listPerson'),
	re_path(r'^listPhone$', PhoneList.as_view(), name='listPhone'),
	re_path(r'^listMeetingPoint$', MeetingPointList.as_view(), name='listMeetingPoint'),
]