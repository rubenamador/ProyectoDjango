from django.shortcuts import render
from django.views.generic import ListView

from apps.Graphs.models import Graph

# Create your views here.

class GraphList(ListView):
	model = Graph
	template_name = 'graphs/graph_list.html'
