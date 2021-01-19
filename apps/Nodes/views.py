from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from apps.Nodes.forms import PersonForm
from apps.Nodes.models import Person, Phone, MeetingPoint

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