from django.shortcuts import render
from django.views.generic import ListView

from apps.Nodes.models import Person

# Create your views here.

class PersonList(ListView):
	model = Person
	template_name = 'nodes/person_list.html'
