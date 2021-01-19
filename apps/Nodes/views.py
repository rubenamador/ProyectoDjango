from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.Nodes.forms import PersonForm, PhoneForm, MeetingPointForm
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

def all_people_delete(request):
	if request.method == 'POST':
		Person.objects.all().delete()
		return redirect('Nodes:listPerson')
	return render(request, 'nodes/all_people_delete.html')
