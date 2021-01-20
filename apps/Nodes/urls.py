from django.urls import re_path
from apps.Nodes.views import PersonList, PersonCreate, PersonUpdate, PersonDelete, PersonAPI
from apps.Nodes.views import PhoneList, PhoneCreate, PhoneUpdate, PhoneDelete, PhoneAPI
from apps.Nodes.views import MeetingPointList, MeetingPointCreate, MeetingPointUpdate, MeetingPointDelete, MeetingPointAPI
from apps.Nodes.views import all_people_delete, all_phones_delete, all_meeting_points_delete

urlpatterns = [
	re_path(r'^newPerson$', PersonCreate.as_view(), name='newPerson'),
	re_path(r'^newPhone$', PhoneCreate.as_view(), name='newPhone'),
	re_path(r'^newMeetingPoint$', MeetingPointCreate.as_view(), name='newMeetingPoint'),
	re_path(r'^listPerson$', PersonList.as_view(), name='listPerson'),
	re_path(r'^listPhone$', PhoneList.as_view(), name='listPhone'),
	re_path(r'^listMeetingPoint$', MeetingPointList.as_view(), name='listMeetingPoint'),
	re_path(r'^editPerson/(?P<pk>[\w|\W]+)/$', PersonUpdate.as_view(), name='editPerson'),
	re_path(r'^editPhone/(?P<pk>[\w|\W]+)/$', PhoneUpdate.as_view(), name='editPhone'),
	re_path(r'^editMeetingPoint/(?P<pk>[\w|\W]+)/$', MeetingPointUpdate.as_view(), name='editMeetingPoint'),
	re_path(r'^deletePerson/(?P<pk>[\w|\W]+)/$', PersonDelete.as_view(), name='deletePerson'),
	re_path(r'^deletePhone/(?P<pk>[\w|\W]+)/$', PhoneDelete.as_view(), name='deletePhone'),
	re_path(r'^deleteMeetingPoint/(?P<pk>[\w|\W]+)/$', MeetingPointDelete.as_view(), name='deleteMeetingPoint'),
	re_path(r'^deleteAllPeople$', all_people_delete, name='deleteAllPeople'),
	re_path(r'^deleteAllPhones$', all_phones_delete, name='deleteAllPhones'),
	re_path(r'^deleteAllMeetingPoints$', all_meeting_points_delete, name='deleteAllMeetingPoints'),
	re_path(r'^apiPerson$', PersonAPI.as_view(), name='apiPerson'),
	re_path(r'^apiPhone$', PhoneAPI.as_view(), name='apiPhone'),
	re_path(r'^apiMeetingPoint$', MeetingPointAPI.as_view(), name='apiMeetingPoint'),
]