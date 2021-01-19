from django.urls import re_path
from apps.Links.views import CallList, CallCreate, CallUpdate
from apps.Links.views import MeetingList, MeetingCreate, MeetingUpdate

urlpatterns = [
	re_path(r'^newCall$', CallCreate.as_view(), name='newCall'),
	re_path(r'^newMeeting$', MeetingCreate.as_view(), name='newMeeting'),
	re_path(r'^listCall$', CallList.as_view(), name='listCall'),
	re_path(r'^listMeeting$', MeetingList.as_view(), name='listMeeting'),
	re_path(r'^editCall/(?P<pk>[\w|\W]+)/$', CallUpdate.as_view(), name='editCall'),
	re_path(r'^editMeeting/(?P<pk>[\w|\W]+)/$', MeetingUpdate.as_view(), name='editMeeting'),
]