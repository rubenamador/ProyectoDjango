from django.urls import re_path
from apps.Links.views import CallList, CallCreate
from apps.Links.views import MeetingList, MeetingCreate

urlpatterns = [
	re_path(r'^newCall$', CallCreate.as_view(), name='newCall'),
	re_path(r'^newMeeting$', MeetingCreate.as_view(), name='newMeeting'),
	re_path(r'^listCall$', CallList.as_view(), name='listCall'),
	re_path(r'^listMeeting$', MeetingList.as_view(), name='listMeeting'),
]