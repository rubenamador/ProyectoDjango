from django.urls import re_path
from apps.Links.views import CallList
from apps.Links.views import MeetingList

urlpatterns = [
	re_path(r'^listCall$', CallList.as_view(), name='listCall'),
	re_path(r'^listMeeting$', MeetingList.as_view(), name='listMeeting'),
]