from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from apps.Graphs.forms import GraphForm
from apps.Graphs.models import Graph

# Create your views here.

class GraphList(ListView):
	model = Graph
	template_name = 'graphs/graph_list.html'

class GraphCreate(CreateView):
	model = Graph
	form_class = GraphForm
	template_name = 'graphs/form.html'
	success_url = reverse_lazy('Graphs:listGraph')
