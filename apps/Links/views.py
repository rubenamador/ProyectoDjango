from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from apps.Links.forms import CallForm, MeetingForm
from apps.Links.models import Call, Meeting

# Create your views here.

class CallList(ListView):
	model = Call
	template_name = 'links/call_list.html'

class MeetingList(ListView):
	model = Meeting
	template_name = 'links/meeting_list.html'

class CallCreate(CreateView):
	model = Call
	form_class = CallForm
	template_name = 'links/form.html'
	success_url = reverse_lazy('Links:listCall')

class MeetingCreate(CreateView):
	model = Meeting
	form_class = MeetingForm
	template_name = 'links/form.html'
	success_url = reverse_lazy('Links:listMeeting')
