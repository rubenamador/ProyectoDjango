from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from rest_framework.views import APIView

from apps.Graphs.forms import GraphForm
from apps.Graphs.models import Graph
from apps.Graphs.serializers import GraphSerializer

import json

# Create your views here.

class GraphList(ListView):
	model = Graph
	template_name = 'graphs/graph_list.html'

class GraphCreate(CreateView):
	model = Graph
	form_class = GraphForm
	template_name = 'graphs/form.html'
	success_url = reverse_lazy('Graphs:listGraph')

class GraphUpdate(UpdateView):
	model = Graph
	form_class = GraphForm
	template_name = 'graphs/form.html'
	success_url = reverse_lazy('Graphs:listGraph')

class GraphDelete(DeleteView):
	model = Graph
	template_name = 'graphs/graph_delete.html'
	success_url = reverse_lazy('Graphs:listGraph')

def all_graphs_delete(request):
	if request.method == 'POST':
		Graph.objects.all().delete()
		return redirect('Graphs:listGraph')
	return render(request, 'graphs/all_graphs_delete.html')

class GraphAPI(APIView):
	serializer = GraphSerializer
	
	def get(self, request, format=None):
		list = Graph.objects.all()
		response = self.serializer(list, many=True)
		
		return HttpResponse(json.dumps(response.data), content_type='application/json')
