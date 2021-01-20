from django.urls import re_path
from apps.Links.views import CallList, CallCreate, CallUpdate, CallDelete, CallAPI
from apps.Links.views import MeetingList, MeetingCreate, MeetingUpdate, MeetingDelete, MeetingAPI
from apps.Links.views import all_calls_delete, all_meetings_delete

urlpatterns = [
	re_path(r'^newCall$', CallCreate.as_view(), name='newCall'),
	re_path(r'^newMeeting$', MeetingCreate.as_view(), name='newMeeting'),
	re_path(r'^listCall$', CallList.as_view(), name='listCall'),
	re_path(r'^listMeeting$', MeetingList.as_view(), name='listMeeting'),
	re_path(r'^editCall/(?P<pk>[\w|\W]+)/$', CallUpdate.as_view(), name='editCall'),
	re_path(r'^editMeeting/(?P<pk>[\w|\W]+)/$', MeetingUpdate.as_view(), name='editMeeting'),
	re_path(r'^deleteCall/(?P<pk>[\w|\W]+)/$', CallDelete.as_view(), name='deleteCall'),
	re_path(r'^deleteMeeting/(?P<pk>[\w|\W]+)/$', MeetingDelete.as_view(), name='deleteMeeting'),
	re_path(r'^deleteAllCalls$', all_calls_delete, name='deleteAllCalls'),
	re_path(r'^deleteAllMeetings$', all_meetings_delete, name='deleteAllMeetings'),
	re_path(r'^apiCall$', CallAPI.as_view(), name='apiCall'),
	re_path(r'^apiMeeting$', MeetingAPI.as_view(), name='apiMeeting'),
]