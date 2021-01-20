from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from rest_framework.views import APIView

from apps.Links.forms import CallForm, MeetingForm
from apps.Links.models import Call, Meeting
from apps.Links.serializers import CallSerializer, MeetingSerializer

import json

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

class CallUpdate(UpdateView):
	model = Call
	form_class = CallForm
	template_name = 'links/form.html'
	success_url = reverse_lazy('Links:listCall')

class MeetingUpdate(UpdateView):
	model = Meeting
	form_class = MeetingForm
	template_name = 'links/form.html'
	success_url = reverse_lazy('Links:listMeeting')

class CallDelete(DeleteView):
	model = Call
	template_name = 'links/call_delete.html'
	success_url = reverse_lazy('Links:listCall')

class MeetingDelete(DeleteView):
	model = Meeting
	template_name = 'links/meeting_delete.html'
	success_url = reverse_lazy('Links:listMeeting')
	
def all_calls_delete(request):
	if request.method == 'POST':
		Call.objects.all().delete()
		return redirect('Links:listCall')
	return render(request, 'links/all_calls_delete.html')

def all_meetings_delete(request):
	if request.method == 'POST':
		Meeting.objects.all().delete()
		return redirect('Links:listMeeting')
	return render(request, 'links/all_meetings_delete.html')

class CallAPI(APIView):
	serializer = CallSerializer
	
	def get(self, request, format=None):
		list = Call.objects.all()
		response = self.serializer(list, many=True)
		
		return HttpResponse(json.dumps(response.data), content_type='application/json')
		
class MeetingAPI(APIView):
	serializer = MeetingSerializer
	
	def get(self, request, format=None):
		list = Meeting.objects.all()
		response = self.serializer(list, many=True)
		
		return HttpResponse(json.dumps(response.data), content_type='application/json')
