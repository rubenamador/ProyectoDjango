from django.shortcuts import render
from django.views.generic import ListView

from apps.Links.models import Call, Meeting

# Create your views here.

class CallList(ListView):
	model = Call
	template_name = 'links/call_list.html'

class MeetingList(ListView):
	model = Meeting
	template_name = 'links/meeting_list.html'
