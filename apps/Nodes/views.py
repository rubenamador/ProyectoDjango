from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from rest_framework.views import APIView

from apps.Nodes.forms import PersonForm, PhoneForm, MeetingPointForm
from apps.Nodes.models import Person, Phone, MeetingPoint
from apps.Nodes.serializers import PersonSerializer, PhoneSerializer, MeetingPointSerializer

import json

# Create your views here.

class PersonList(ListView):
	model = Person
	template_name = 'nodes/person_list.html'

class PhoneList(ListView):
	model = Phone
	template_name = 'nodes/phone_list.html'

class MeetingPointList(ListView):
	model = MeetingPoint
	template_name = 'nodes/meeting_point_list.html'

class PersonCreate(CreateView):
	model = Person
	form_class = PersonForm
	template_name = 'nodes/form.html'
	success_url = reverse_lazy('Nodes:listPerson')

class PhoneCreate(CreateView):
	model = Phone
	form_class = PhoneForm
	template_name = 'nodes/form.html'
	success_url = reverse_lazy('Nodes:listPhone')

class MeetingPointCreate(CreateView):
	model = MeetingPoint
	form_class = MeetingPointForm
	template_name = 'nodes/form.html'
	success_url = reverse_lazy('Nodes:listMeetingPoint')

class PersonUpdate(UpdateView):
	model = Person
	form_class = PersonForm
	template_name = 'nodes/form.html'
	success_url = reverse_lazy('Nodes:listPerson')

class PhoneUpdate(UpdateView):
	model = Phone
	form_class = PhoneForm
	template_name = 'nodes/form.html'
	success_url = reverse_lazy('Nodes:listPhone')

class MeetingPointUpdate(UpdateView):
	model = MeetingPoint
	form_class = MeetingPointForm
	template_name = 'nodes/form.html'
	success_url = reverse_lazy('Nodes:listMeetingPoint')

class PersonDelete(DeleteView):
	model = Person
	template_name = 'nodes/person_delete.html'
	success_url = reverse_lazy('Nodes:listPerson')

class PhoneDelete(DeleteView):
	model = Phone
	template_name = 'nodes/phone_delete.html'
	success_url = reverse_lazy('Nodes:listPhone')

class MeetingPointDelete(DeleteView):
	model = MeetingPoint
	template_name = 'nodes/meeting_point_delete.html'
	success_url = reverse_lazy('Nodes:listMeetingPoint')

def all_people_delete(request):
	if request.method == 'POST':
		Person.objects.all().delete()
		return redirect('Nodes:listPerson')
	return render(request, 'nodes/all_people_delete.html')
	
def all_phones_delete(request):
	if request.method == 'POST':
		Phone.objects.all().delete()
		return redirect('Nodes:listPhone')
	return render(request, 'nodes/all_phones_delete.html')

def all_meeting_points_delete(request):
	if request.method == 'POST':
		MeetingPoint.objects.all().delete()
		return redirect('Nodes:listMeetingPoint')
	return render(request, 'nodes/all_meeting_points_delete.html')

class PersonAPI(APIView):
	serializer = PersonSerializer
	
	def get(self, request, format=None):
		list = Person.objects.all()
		response = self.serializer(list, many=True)
		
		return HttpResponse(json.dumps(response.data), content_type='application/json')

class PhoneAPI(APIView):
	serializer = PhoneSerializer
	
	def get(self, request, format=None):
		list = Phone.objects.all()
		response = self.serializer(list, many=True)
		
		return HttpResponse(json.dumps(response.data), content_type='application/json')

class MeetingPointAPI(APIView):
	serializer = MeetingPointSerializer
	
	def get(self, request, format=None):
		list = MeetingPoint.objects.all()
		response = self.serializer(list, many=True)
		
		return HttpResponse(json.dumps(response.data), content_type='application/json')
