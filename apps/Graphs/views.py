from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from rest_framework.views import APIView

from apps.Graphs.forms import GraphForm, PersonForm, PhoneForm, MeetingPointForm
from apps.Graphs.models import Graph
from apps.Graphs.serializers import GraphSerializer

from apps.Nodes.models import Person, Phone, MeetingPoint
from apps.Links.models import Call, Meeting

import json
import fileinput
import pymongo
from pymongo import MongoClient
from random import randint
import math

import time
import networkx as nx
import pickle

# Create your views here.

def main_page(request):
	return render(request, 'graphs/graph_list.html')

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

class GraphView(ListView):
	model = Graph
	template_name = 'graphs/graph_view.html'
	
	def get_context_data(self, **kwargs):
		context = super(GraphView, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk', 0)
		graph = self.model.objects.get(id=pk)
		context['graph'] = graph
		
		context['people'] = Person.objects.all()
		context['phones'] = Phone.objects.all()
		context['points'] = MeetingPoint.objects.all()
		context['calls'] = Call.objects.all()
		context['meetings'] = Meeting.objects.all()
		context['ownerships'] = Phone.objects.all()
		
		return context
		
def random_graph_create(request):
	if request.method == 'POST':
		person_size = Person.objects.count()
		meeting_point_size = MeetingPoint.objects.count()
		call_size = Call.objects.count()
		meeting_size = Meeting.objects.count()
		random_graph(person_size, meeting_point_size, call_size, meeting_size)
		return redirect('Graphs:listGraph')
	return render(request, 'graphs/random_graph_create.html')
	
class DegreeForm(FormView):
	model = Graph
	form_class = PersonForm
	template_name = 'graphs/degree_form.html'
	
	def get_context_data(self, **kwargs):
		context = super(DegreeForm, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk', 0)
		graph = self.model.objects.get(id=pk)
		context['graph'] = graph
		
		context['people'] = Person.objects.all()
		context['phones'] = Phone.objects.all()
		context['points'] = MeetingPoint.objects.all()
		context['form2'] = PhoneForm
		context['form3'] = MeetingPointForm
		return context
	
class DegreePersonView(ListView):
	model = Graph
	template_name = 'graphs/graph_view.html'
	
	def get_context_data(self, **kwargs):
		context = super(DegreePersonView, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk', 0)
		graph = self.model.objects.get(id=pk)
		context['graph'] = graph
		pk2 = self.kwargs.get('pk2', 0)
		node = Person.objects.get(id=pk2)
		context['node'] = node
		
		people = Person.objects.all()
		phones = Phone.objects.all()
		points = MeetingPoint.objects.all()
		calls = Call.objects.all()
		meetings = Meeting.objects.all()
		dict = search_person_degree(node, people, phones, points, calls, meetings)
		
		context['people'] = dict['people']
		context['phones'] = dict['phones']
		context['points'] = dict['points']
		context['calls'] = dict['calls']
		context['meetings'] = dict['meetings']
		context['ownerships'] = dict['ownerships']
		context['value'] = dict['value']
		
		return context
		
class DegreePhoneView(ListView):
	model = Graph
	template_name = 'graphs/graph_view.html'
	
	def get_context_data(self, **kwargs):
		context = super(DegreePhoneView, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk', 0)
		graph = self.model.objects.get(id=pk)
		context['graph'] = graph
		pk2 = self.kwargs.get('pk2', 0)
		node = Phone.objects.get(number=pk2)
		context['node'] = node
		
		people = Person.objects.all()
		phones = Phone.objects.all()
		points = MeetingPoint.objects.all()
		calls = Call.objects.all()
		meetings = Meeting.objects.all()
		dict = search_phone_degree(node, people, phones, points, calls, meetings)
		
		context['people'] = dict['people']
		context['phones'] = dict['phones']
		context['points'] = dict['points']
		context['calls'] = dict['calls']
		context['meetings'] = dict['meetings']
		context['ownerships'] = dict['ownerships']
		context['value'] = dict['value']
		
		return context
		
class DegreeMeetingPointView(ListView):
	model = Graph
	template_name = 'graphs/graph_view.html'
	
	def get_context_data(self, **kwargs):
		context = super(DegreeMeetingPointView, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk', 0)
		graph = self.model.objects.get(id=pk)
		context['graph'] = graph
		pk2 = self.kwargs.get('pk2', 0)
		node = MeetingPoint.objects.get(id=pk2)
		context['node'] = node
		
		people = Person.objects.all()
		phones = Phone.objects.all()
		points = MeetingPoint.objects.all()
		calls = Call.objects.all()
		meetings = Meeting.objects.all()
		dict = search_point_degree(node, people, phones, points, calls, meetings)
		
		context['people'] = dict['people']
		context['phones'] = dict['phones']
		context['points'] = dict['points']
		context['calls'] = dict['calls']
		context['meetings'] = dict['meetings']
		context['ownerships'] = dict['ownerships']
		context['value'] = dict['value']
		
		return context



class DegreeGraph(ListView):
	model = Graph
	template_name = 'graphs/centrality_graph_view.html'
	
	def get_context_data(self, **kwargs):
		context = super(DegreeGraph, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk', 0)
		graph = self.model.objects.get(id=pk)
		context['graph'] = graph
		
		people = Person.objects.all()
		phones = Phone.objects.all()
		points = MeetingPoint.objects.all()
		calls = Call.objects.all()
		meetings = Meeting.objects.all()
		
		dict = search_graph_degree(people, phones, points, calls, meetings)
		
		context['people'] = dict['people']
		context['phones'] = dict['phones']
		context['points'] = dict['points']
		context['calls'] = calls
		context['meetings'] = meetings
		context['ownerships'] = phones
		context['max_value'] = dict['max_value']
		
		return context

class PathForm(FormView):
	model = Graph
	form_class = PersonForm
	template_name = 'graphs/path_form.html'
	
	def get_context_data(self, **kwargs):
		context = super(PathForm, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk', 0)
		graph = self.model.objects.get(id=pk)
		context['graph'] = graph
		
		context['people'] = Person.objects.all()
		context['phones'] = Phone.objects.all()
		context['points'] = MeetingPoint.objects.all()
		context['form2'] = PhoneForm
		context['form3'] = MeetingPointForm
		return context
		
class PathView(ListView):
	model = Graph
	template_name = 'graphs/graph_view.html'
	
	def get_context_data(self, **kwargs):
		context = super(PathView, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk', 0)
		graph = self.model.objects.get(id=pk)
		context['graph'] = graph
		
		pk2 = self.kwargs.get('pk2', 0)
		source = get_model_object_by_id(pk2)
		context['node'] = source
		
		pk3 = self.kwargs.get('pk3', 0)
		dest = get_model_object_by_id(pk3)
		context['dest'] = dest
		
		people = Person.objects.all()
		phones = Phone.objects.all()
		points = MeetingPoint.objects.all()
		calls = Call.objects.all()
		meetings = Meeting.objects.all()

		G = get_graph(people, phones, points, calls, meetings)
		try:
			path = nx.shortest_path(G, source=source , target=dest)
		except nx.NetworkXNoPath:
			path = []
		
		dict = {}
		dict['people'] = []
		dict['phones'] = []
		dict['points'] = []
		dict['calls'] = []
		dict['meetings'] = []
		dict['ownerships'] = []
		add_nodes_of_path(path, dict, calls, meetings, phones)
		
		context['people'] = dict['people']
		context['phones'] = dict['phones']
		context['points'] = dict['points']
		context['calls'] = dict['calls']
		context['meetings'] = dict['meetings']
		context['ownerships'] = dict['ownerships']
		
		return context

class ClosenessPersonForm(FormView):
	model = Graph
	form_class = PersonForm
	template_name = 'graphs/person_form.html'
	
	def get_context_data(self, **kwargs):
		context = super(ClosenessPersonForm, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk', 0)
		graph = self.model.objects.get(id=pk)
		context['graph'] = graph
		context['people'] = Person.objects.all()
		return context
		
class ClosenessPhoneForm(FormView):
	model = Graph
	form_class = PhoneForm
	template_name = 'graphs/phone_form.html'
	
	def get_context_data(self, **kwargs):
		context = super(ClosenessPhoneForm, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk', 0)
		graph = self.model.objects.get(id=pk)
		context['graph'] = graph
		context['phones'] = Phone.objects.all()
		return context
		
class ClosenessMeetingPointForm(FormView):
	model = Graph
	form_class = MeetingPointForm
	template_name = 'graphs/meeting_point_form.html'
	
	def get_context_data(self, **kwargs):
		context = super(ClosenessMeetingPointForm, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk', 0)
		graph = self.model.objects.get(id=pk)
		context['graph'] = graph
		context['meeting_points'] = MeetingPoint.objects.all()
		return context

class ClosenessView(ListView):
	model = Graph
	template_name = 'graphs/graph_view.html'
	
	def get_context_data(self, **kwargs):
		context = super(ClosenessView, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk', 0)
		graph = self.model.objects.get(id=pk)
		context['graph'] = graph
		pk2 = self.kwargs.get('pk2', 0)
		node = get_model_object_by_id(pk2)
		context['node'] = node
		
		people = Person.objects.all()
		phones = Phone.objects.all()
		points = MeetingPoint.objects.all()
		calls = Call.objects.all()
		meetings = Meeting.objects.all()
		dict = search_closeness(node, people, phones, points, calls, meetings)
		
		context['people'] = dict['people']
		context['phones'] = dict['phones']
		context['points'] = dict['points']
		context['calls'] = dict['calls']
		context['meetings'] = dict['meetings']
		context['ownerships'] = dict['ownerships']
		context['value'] = dict['value']
		
		return context

class ClosenessGraph(ListView):
	model = Graph
	template_name = 'graphs/centrality_graph_view.html'
	
	def get_context_data(self, **kwargs):
		context = super(ClosenessGraph, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk', 0)
		graph = self.model.objects.get(id=pk)
		context['graph'] = graph
		
		people = Person.objects.all()
		phones = Phone.objects.all()
		points = MeetingPoint.objects.all()
		calls = Call.objects.all()
		meetings = Meeting.objects.all()
		
		dict = search_graph_closeness(people, phones, points, calls, meetings)
		
		context['people'] = dict['people']
		context['phones'] = dict['phones']
		context['points'] = dict['points']
		context['calls'] = calls
		context['meetings'] = meetings
		context['ownerships'] = phones
		context['max_value'] = dict['max_value']
		
		return context

class BetweenessGraph(ListView):
	model = Graph
	template_name = 'graphs/centrality_graph_view.html'
	
	def get_context_data(self, **kwargs):
		context = super(BetweenessGraph, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk', 0)
		graph = self.model.objects.get(id=pk)
		context['graph'] = graph
		
		people = Person.objects.all()
		phones = Phone.objects.all()
		points = MeetingPoint.objects.all()
		calls = Call.objects.all()
		meetings = Meeting.objects.all()
		
		dict = search_graph_betweeness(people, phones, points, calls, meetings)
		
		context['people'] = dict['people']
		context['phones'] = dict['phones']
		context['points'] = dict['points']
		context['calls'] = calls
		context['meetings'] = meetings
		context['ownerships'] = phones
		context['max_value'] = dict['max_value']
		
		return context

class EigenvectorGraph(ListView):
	model = Graph
	template_name = 'graphs/centrality_graph_view.html'
	
	def get_context_data(self, **kwargs):
		context = super(EigenvectorGraph, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk', 0)
		graph = self.model.objects.get(id=pk)
		context['graph'] = graph
		
		people = Person.objects.all()
		phones = Phone.objects.all()
		points = MeetingPoint.objects.all()
		calls = Call.objects.all()
		meetings = Meeting.objects.all()
		
		dict = search_graph_eigenvector(people, phones, points, calls, meetings)
		
		context['people'] = dict['people']
		context['phones'] = dict['phones']
		context['points'] = dict['points']
		context['calls'] = calls
		context['meetings'] = meetings
		context['ownerships'] = phones
		context['max_value'] = dict['max_value']
		
		return context

class HarmonyGraph(ListView):
	model = Graph
	template_name = 'graphs/centrality_graph_view.html'
	
	def get_context_data(self, **kwargs):
		context = super(HarmonyGraph, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk', 0)
		graph = self.model.objects.get(id=pk)
		context['graph'] = graph
		
		people = Person.objects.all()
		phones = Phone.objects.all()
		points = MeetingPoint.objects.all()
		calls = Call.objects.all()
		meetings = Meeting.objects.all()
		
		dict = search_graph_harmony(people, phones, points, calls, meetings)
		
		context['people'] = dict['people']
		context['phones'] = dict['phones']
		context['points'] = dict['points']
		context['calls'] = calls
		context['meetings'] = meetings
		context['ownerships'] = phones
		context['max_value'] = dict['max_value']
		
		return context

class KatzGraph(ListView):
	model = Graph
	template_name = 'graphs/centrality_graph_view.html'
	
	def get_context_data(self, **kwargs):
		context = super(KatzGraph, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk', 0)
		graph = self.model.objects.get(id=pk)
		context['graph'] = graph
		
		people = Person.objects.all()
		phones = Phone.objects.all()
		points = MeetingPoint.objects.all()
		calls = Call.objects.all()
		meetings = Meeting.objects.all()
		
		dict = search_graph_katz(people, phones, points, calls, meetings)
		
		context['people'] = dict['people']
		context['phones'] = dict['phones']
		context['points'] = dict['points']
		context['calls'] = calls
		context['meetings'] = meetings
		context['ownerships'] = phones
		context['max_value'] = dict['max_value']
		
		return context
		
		
#################################################################################
""" Functions used in views """
#################################################################################


def random_graph(last_person_id, last_point_id, last_call_id, last_meeting_id):
	
	#Añadiendo personas al grafo
	number_of_people = randint(1, 10)
	data = ""
	
	for i in range(number_of_people):
		person_name = get_random_name()
		person_surname = get_random_surname()
		person_id = last_person_id + i
		evalue_id(person_id, Person)
				
		Person.objects.create(id="person:" + str(person_id), name=person_name, surname=person_surname)

	#Añadiendo telefonos al grafo
	number_of_phones = randint(1, 10)
	data = ""
	
	for i in range(number_of_phones):
		phone_number = get_random_phone_number()
		owner_name = get_random_person()
		
		Phone.objects.create(number=phone_number, owner=owner_name)

	#Añadiendo puntos de reunion al grafo
	number_of_points = randint(1, 10)
	data = ""
	
	for i in range(number_of_points):
		point_place = None
		point_date = None
		point_time = None
		
		existMeeting = True
		while(existMeeting):
			point_place = get_random_place()
			point_date = get_random_date()
			point_time = get_random_time()
			existMeeting = False
			points = MeetingPoint.objects.all()
			for point in points:
				if(point.place == point_place and point.date == point_date and point.time == point_time):
					existMeeting = True
		point_id = last_point_id + i
		evalue_id(point_id, MeetingPoint)
		
		MeetingPoint.objects.create(id="point:" + str(point_id), place=point_place, date=point_date, time=point_time)

	#Añadiendo llamadas al grafo
	number_of_calls = randint(1, 10)
	data = ""
	
	for i in range(number_of_calls):
		call_phone_1 = get_random_phone()
		call_phone_2 = get_random_phone()
		call_id = last_call_id + i
		evalue_id(call_id, Call)
		
		Call.objects.create(id="call:" + str(call_id), phone_1=call_phone_1, phone_2=call_phone_2)

	#Añadiendo reuniones al grafo
	number_of_meetings = 0
	data = ""
	if(number_of_people > number_of_points):
		number_of_meetings = randint(1, number_of_people)
	else:
		number_of_meetings = randint(1, number_of_points)
	
	
	for i in range(number_of_meetings):
		person = None
		point = None
		
		existMeeting = True
		while(existMeeting):
			meeting_person = get_random_person()
			meeting_point = get_random_point()
			existMeeting = False
			meetings = Meeting.objects.all()
			for meeting in meetings:
				if(meeting.person.id == person and meeting.point.id == point):
					existMeeting = True
		meeting_id = last_meeting_id + i
		evalue_id(meeting_id, Meeting)
		
		Meeting.objects.create(id="meeting:" + str(meeting_id), person=meeting_person, point=meeting_point)

def mongoimport(host, port, db, collection, file):
	client = MongoClient(host, port)
	db = client[db]
	collection_currency = db[collection]
	
	with open(file) as f:
		file_data = json.load(f)
	
	collection_currency.insert(file_data)
	client.close()
	
def evalue_id(id, model):
	exist = True
	while(exist):
		exist = False
		#print(exist)
		try:
			if(model == "<class 'apps.Nodes.models.Person'>"):
				model.objects.get(id="person:" + str(id))
			elif(model == "<class 'apps.Nodes.models.MeetingPoint'>"):
				model.objects.get(id="point:" + str(id))
			elif(model == "<class 'apps.Links.models.Call'>"):
				model.objects.get(id="call:" + str(id))
			elif(model == "<class 'apps.Links.models.Meeting'>"):
				model.objects.get(id="meeting:" + str(id))
		except model.DoesNotExist:
			id = id + 1
			exist = True

def get_random_name():
	names = ['Aaron',
	'Abderraman', 'Abdon', 'Abel', 'Abelardo', 'Abigail', 'Abraham', 'Abram', 'Abril', 
	'Adan', 'Adela', 'Adelaida', 'Adolfo', 'Adon', 'Adonis', 'Adrian', 'Adriana', 'Adriano', 
	'Africa', 'Afrodita', 
	'Agamenon', 'Agata', 'Agenor', 'Agripina', 'Agustin' 
	'Aida', 'Aihnoa', 'Aitana', 'Aitor', 
	'Ajax', 
	'Akenaton', 
	'Ala', 'Aladin', 'Aladina', 'Aladino', 'Alarico', 'Alba', 'Alberto', 'Aldo', 'Alejandra', 'Alejandro', 'Alejo', 'Alexandra', 'Alfonso', 'Alfredo', 'Ali', 'Alicia', 'Almanzor', 'Almudena', 'Alonso', 'Altair', 'Alvaro',
	'Amadeo', 'Amador', 'Amaia', 'Amalia', 'Amancio', 'Amanda', 'Amaya', 'Ambrosio', 'Amelia', 'Amenofis', 'America', 'Americo', 'Amilcar', 'Amparo',
	'Ana', 'Anacleto', 'Anastasia', 'Anaximandro', 'Andrea', 'Andres', 'Angel', 'Angela', 'Anibal', 'Aniceto', 'Anselmo', 'Antigona', 'Antiope', 'Anton', 'Antonio', 'Anubis',
	'Aparicio', 'Apolo',
	'Aquileo', 'Aquiles', 'Aquilino',
	'Araceli', 'Aragorn', 'Arantxa', 'Arcadio', 'Ares', 'Ariadna', 'Ariadne', 'Ariana', 'Ariel', 'Aristo', 'Aristoteles', 'Armando', 'Arnaldo', 'Arquimedes', 'Artajerjes', 'Artemisa', 'Arturo',
	'Asdrubal', 'Asier', 'Astarte', 'Asterix', 'Asubanipal',
	'Atahualpa', 'Atenea', 'Atila',
	'Augusto', 'Aura', 'Aurelia', 'Aurelio', 'Aurora',
	'Avelino',
	'Axel',
	'Azazel', 'Azrael', 'Azucena',
	
	'Baal', 'Baco', 'Baldomero', 'Baltasar', 'Barbara', 'Barrabas', 'Bartimeo', 'Bartolome', 'Basilio', 'Bastet', 'Bastian', 
	'Bea', 'Beatriz', 'Bebo', 'Begoña', 'Belen', 'Belinda', 'Bella', 'Beltran', 'Benedicto', 'Benicio', 'Benigno', 'Benito', 'Benjamin', 'Berengario', 'Bernabe', 'Bernadette', 'Bernarda', 'Bernardina', 'Bernardino', 'Bernardo', 'Berta', 'Bertin', 'Berto',
	'Bianca', 'Bibiana', 'Bilbo', 'Bizas',
	'Bjorn',
	'Blanca', 'Blas', 'Blasa', 'Blasco',
	'Boadicea', 'Bonifacio', 'Boris', 'Boromir', 'Bosco',
	'Brahma', 'Bran', 'Brando', 'Braulio', 'Brenda', 'Brian', 'Brigida', 'Brisa', 'Brunilda', 'Bruno', 'Bruto',
	'Buda', 'Buenaventura',
	
	'Cain', 'Caligula', 'Calixto', 'Camila', 'Camilo', 'Candela', 'Candida', 'Candido', 'Caridad', 'Carina', 'Carla', 'Carlos', 'Carmela', 'Carmelo', 'Carmen', 'Carmina', 'Carolina', 'Casandra', 'Casimiro', 'Castor', 'Catalina', 'Catalino', 'Cayetana', 'Cayetano',
	'Cecilia', 'Cecilio', 'Cefas', 'Celedonio', 'Celeste', 'Celia', 'Celso', 'Cenicienta', 'Cesar',
	'Charo', 'Chema', 'Chenoa', 'Chindasvinta', 'Chindasvinto',
	'Ciara', 'Ciceron', 'Cintia', 'Cipriano', 'Cirilo', 'Ciro',
	'Clara', 'Claudia', 'Claudio', 'Clemente', 'Cleopatra', 'Clodoveo', 'Clotilde', 
	'Cochise', 'Concepcion', 'Conrado', 'Constante', 'Constantino', 'Consuelo', 'Copernico', 'Cora', 'Cornelio', 'Covadonga',
	'Crispin', 'Cristian', 'Cristiano', 'Cristina', 'Cristobal', 
	'Cupido', 
	'Cyrano',
	
	'Dafne', 'Dagon', 'Dalila', 'Damaso', 'Damian', 'Dan', 'Danae', 'Daniel', 'Daniela', 'Danilo', 'Dante', 'Dario', 'Dastan', 'David', 'Dayana', 'Dazbog',
	'Debora', 'Demetrio',  'Democrates', 'Democrito', 'Denis', 'Desire', 'Dexter', 'Deyanira',
	'Diana', 'Diego', 'Dimas', 'Dimitri', 'Dinio', 'Diocleciano', 'Diogenes', 'Dioniso',
	'Dolores', 'Domingo', 'Donato', 'Dora', 'Dorotea', 'Doroteo',
	'Draco',
	'Dulce',
	
	'Edgar', 'Edgardo', 'Edipo', 'Edmundo', 'Edna', 'Edson', 'Eduardo', 'Edurne',
	'Efrain', 'Efren',
	'Eladio', 'Electra', 'Elena', 'Eleonor', 'Elias', 'Elisa', 'Eliseo', 'Elmer', 'Elmo', 'Eloy', 'Elpidio', 'Elsa', 'Elvira', 'Elvis',
	'Emanuel', 'Emilia', 'Emilio', 'Emma',
	'Encarna', 'Eneas', 'Enoc', 'Enrico', 'Enrique', 'Enriqueta', 'Enzo',
	'Epicuro', 'Epifanio', 'Epimeteo',
	'Erasmo', 'Eric', 'Erico', 'Erik', 'Erika', 'Ernesto', 'Eros',
	'Esau', 'Escarlata', 'Esmeralda', 'Esopo', 'Espartaco', 'Esperanza', 'Estanislao', 'Esteban', 'Estefania', 'Estela', 'Ester',
	'Eugenia', 'Eugenio', 'Eulogio', 'Eusebio', 'Eustaquio',
	'Eva', 'Evaristo', 'Evelyn', 'Evo',
	'Ezequiel', 'Ezio',
	
	'Fabian', 'Fabiana', 'Fabiano', 'Fabio', 'Fabiola', 'Fabricio', 'Fabrique', 'Falbala', 'Fanny', 'Faustina', 'Faustino', 'Fausto',
	'Febo', 'Federica', 'Federico', 'Felicia', 'Feliciano', 'Felicidad', 'Felipe', 'Felisa', 'Felix', 'Ferdinando', 'Fermin', 'Fernan','Fernanda', 'Fernando',
	'Fidel', 'Filemon', 'Filipo', 'Fina', 'Fiodor', 'Fiona', 
	'Flavia', 'Flavio', 'Florencio', 'Florencia', 'Florentino', 'Francia', 'Francisca', 'Francisco', 'Fredo', 'Frida', 'Frodo',
	'Fulgencio',
	
	'Gabino', 'Gabriel', 'Gabriela', 'Galeno', 'Galilea', 'Galileo', 'Gandalf', 'Ganesha', 'Garcilaso', 'Gaspar', 'Gaston',
	'Gea', 'Gedeon', 'Gemma', 'Genesis', 'Genoveva', 'Georgia', 'Gepeto', 'Gerardo', 'German', 'Geronimo', 'Gertrudis', 'Gervasio',
	'Giacomo', 'Gilberta', 'Gilda', 'Ginebra', 'Giogia', 'Giorgio', 'Giovanni', 'Gisela',
	'Glenda', 'Gloria',
	'Godofredo', 'Goliat', 'Gonzalo',
	'Graciela', 'Grecia', 'Gregoria', 'Gregorio', 'Greta', 'Gretel', 'Griselda',
	'Guadalupe', 'Guillermina', 'Guillermo', 'Gurgundofora', 'Gustavo', 'Guzman',
	
	'Hades', 'Hammurabi', 'Hanibal', 'Hansel',
	'Hector', 'Hefesto', 'Heidi', 'Heihachi', 'Helen', 'Helena', 'Heleno', 'Helia', 'Helio', 'Hera', 'Heracles', 'Hercules', 'Heredoto', 'Hermes', 'Herminia', 'Herminio', 'Hernan', 'Hernanda', 'Hernando', 'Herodes',
	'Hilario', 'Hipocrates', 'Hipolita', 'Hipolito',
	'Homero', 'Honorato', 'Honorio', 'Horacio', 'Hortensia', 'Horus',
	'Hugo',
	
	'Iago', 'Ian', 'Ianna',
	'Ignacio', 'Igor',
	'Iker',
	'Ildefonsa', 'Ildefonso',
	'Imanol', 'Imelda', 'Imhotep',
	'Inca', 'Indira', 'Ines', 'Ingrid', 'Inma', 'Inna', 'Inocencia', 'Inocencio',
	'Iñaki', 'Iñigo',
	'Irene', 'Ireneo', 'Irina', 'Iris', 'Irma',
	'Isaac', 'Isabel', 'Isabela', 'Isadora', 'Isco', 'Isidoro', 'Isidro', 'Isis', 'Ismael', 'Isolda', 'Israel', 'Isthar',
	'Ivan', 'Ivar', 'Ivonne',
	'Izan',
	
	'Jacinta', 'Jacinto', 'Jacob', 'Jacobo', 'Jade', 'Jaime', 'Jairo', 'James', 'Jared', 'Jareth', 'Jason', 'Jasper', 'Javier', 'Javiera',
	'Jehova', 'Jenaro', 'Jennifer', 'Jeremias', 'Jerjes', 'Jese', 'Jessica', 'Jesus',
	'Jimena',
	'Job', 'Jorge', 'Jose', 'Josefina', 'Josue',
	'Juan', 'Juana', 'Judas', 'Judith', 'Julia', 'Julian', 'Juliana', 'Julieta', 'Julio', 'Juno', 'Jupiter', 'Justiniano', 'Justino', 'Justo',
	
	'Kaio', 'Karim', 'Karina', 'Karl', 'Karlos', 'Katara', 'Katrina', 'Kazuya',
	'Kefren', 'Ken', 'Kendal', 'Kenia', 'Keops', 'Kepler', 'Kevin', 'Khepri', 'Khufu',
	'Kiara', 'Kika', 'Kiko', 'Kira', 'Kirk',
	'Klaus', 'Klever',
	'Koldo',
	'Kratos', 'Krilin', 'Krista', 'Krunilda',
	'Kukulcan', 'Kurt',
	
	'Ladislao', 'Laila', 'Lanzarote', 'Lara', 'Laura', 'Laureano', 'Lazaro',
	'Leandro', 'Legolas', 'Leia', 'Lemuel', 'Leo', 'Leocadio', 'Leogivildo', 'Leon', 'Leonardo', 'Leonidas', 'Leonor', 'Leopoldo', 'Leroy', 'Leticia', 'Leyre',
	'Libia', 'Lidia', 'Lilith', 'Lilo', 'Lina', 'Linda', 'Lisa', 'Lisandro', 'Livio', 'Liz',
	'Logan', 'Loki', 'Lola', 'Loles', 'Lope', 'Lorena', 'Lorenza', 'Lorenzo', 'Loreto', 'Lorna', 'Lotario', 'Lourdes',
	'Luca', 'Lucas', 'Lucero', 'Lucia', 'Luciano', 'Lucifer', 'Lucio', 'Lucrecia', 'Ludovico', 'Luigi', 'Luis', 'Luisa', 'Lujan', 'Luz',
	
	'Macabeo', 'Macarena', 'Macario', 'Madonna', 'Mafalda', 'Magda', 'Magdalena', 'Magnus', 'Mahoma', 'Maite', 'Maitena', 'Malena', 'Mambrino', 'Manco', 'Manel', 'Manfredo', 'Manolo','Manuel', 'Manuela', 'Mark', 'Marcelina', 'Marcelino', 'Marcelo', 'Marcial', 'Marco', 'Marcos', 'Margot', 'Maria', 'Mariana', 'Mariano', 'Maribel', 'Marina', 'Marino', 'Mario', 'Mariola', 'Marion', 'Marisa', 'Marlon', 'Marta', 'Marte', 'Martin','Martina', 'Mateo', 'Matias', 'Matilda', 'Matilde', 'Mauricio', 'Mauro', 'Maxima', 'Maximiliano', 'Maximo',
	'Megan', 'Megara', 'Melchor', 'Melibea', 'Melina', 'Melinda', 'Melquiades', 'Menelao', 'Menes', 'Mercedes', 'Merche', 'Mercurio', 'Merida', 'Merlin', 'Mesias',
	'Micaela', 'Micerinos', 'Michelle', 'Midas', 'Miguel', 'Milagros', 'Milan', 'Milo', 'Mina', 'Minerva', 'Miriam',
	'Moana', 'Moctezuma', 'Modesto', 'Moira', 'Moises', 'Monica', 'Montserrat', 'Morfeo', 'Morgana', 'Morgan', 'Mortadelo',
	'Mufasa', 'Mustafa',
	
	'Nabuco', 'Nabucodonosor', 'Nacho', 'Nadia', 'Nadja', 'Nagore', 'Naim', 'Nala', 'Naomi', 'Napoleon', 'Narcisa', 'Narciso', 'Natalia', 'Natan', 'Natanael', 'Nataniel', 'Natividad',
	'Nefertiti', 'Neftis', 'Nehemias', 'Nelson', 'Nemesio', 'Nemo', 'Neo', 'Neptuno', 'Nerea', 'Nereo', 'Neron', 'Nestor',
	'Nicolas', 'Nicolasa', 'Nieves', 'Nina', 'Nino',
	'Noe', 'Noel', 'Noelia', 'Nora', 'Norberto', 'Norma', 'Norman', 'Normando',
	'Nubia', 'Nun', 'Nuria',
	
	'Obelix', 'Oberon',
	'Oceana', 'Oceano', 'Octavia', 'Octavio',
	'Odin', 'Odisea', 'Odiseo', 'Odoacro', 'Odon', 'Odor',
	'Ofelia',
	'Olaf', 'Olegario', 'Olga', 'Olimpia', 'Oliver', 'Olivia',
	'Omar',
	'Ona', 'Onesima', 'Onesimo', 'Onofre',
	'Orestes', 'Orfeo', 'Oriana', 'Oriol', 'Orlando', 'Ororo', 'Orquidea', 'Orson', 'Ortensia',
	'Oscar', 'Osias', 'Osiris', 'Osman', 'Osvaldo',
	'Otelo', 'Otilio', 'Oton', 'Otto',
	'Ovidio',
	
	'Pablo', 'Paca', 'Paco', 'Paloma', 'Palomo', 'Pamela', 'Pancracio', 'Pandora', 'Panfilo', 'Paris', 'Parmenides', 'Pascal', 'Pascual', 'Patricia', 'Patricio', 'Patroclo', 'Pau', 'Paula', 'Paulina', 'Paulino', 'Paz',
	'Pedro', 'Penelope', 'Pep', 'Pepa', 'Pepe', 'Perceval', 'Pericles', 'Perseo', 'Petra', 'Petronila',
	'Piedad', 'Piero', 'Pietro', 'Pilar', 'Pio',
	'Placido', 'Platon', 'Plinio', 'Plutarco', 'Pluto', 'Pluton',
	'Policarpo', 'Polifemo', 'Polux', 'Pompeyo', 'Poseidon',
	'Priamo', 'Primavera', 'Priscila', 'Prometeo', 'Prudencia', 'Prudencio',
	'Ptah', 'Ptolomeo',
	'Pumba', 'Purificacion',
	
	'Quasimodo', 'Quetzalcoalt', 'Quintin', 'Quinto', 'Quique', 'Quirino',
	
	'Ra', 'Radamel', 'Rafael', 'Rafaela', 'Rafiki', 'Ragnar', 'Raimundo', 'Ramira', 'Ramiro', 'Ramon', 'Ramona', 'Ramses', 'Rapunzel', 'Raquel', 'Ratogenes', 'Raul',
	'Rea', 'Rebeca', 'Recaredo', 'Regina', 'Regulo', 'Reinaldo', 'Remedios', 'Remo', 'Renata', 'Renato',
	'Ricarda', 'Ricardo', 'Rigoberta', 'Rigoberto', 'Rihanna', 'Rita',
	'Roberto', 'Robin', 'Rocinante', 'Rocio', 'Rodolfo', 'Rodrigo', 'Rogelia', 'Rogelio', 'Rolan', 'Rolando', 'Roldan', 'Roma', 'Roman', 'Romeo', 'Romina', 'Romualdo', 'Romulo', 'Ronaldo', 'Roque', 'Rosa', 'Rosalia', 'Rosalinda', 'Rosana', 'Rosario', 'Roselia', 'Rosendo',
	'Ruben', 'Rucio', 'Rudy', 'Ruperta', 'Ruperto', 'Ruth',
	'Ryan',
	
	'Sabe', 'Sabina', 'Sabino', 'Sabio', 'Sabrina', 'Sahara', 'Salma', 'Salome', 'Salomon', 'Salvador', 'Samanta', 'Samira', 'Samuel', 'Sancho', 'Sandra', 'Sandro', 'Sanson', 'Santiago', 'Sara', 'Saray', 'Sargon', 'Satanas', 'Saturnino', 'Saturno', 'Saul', 'Saulo',
	'Sebastian', 'Segismunda', 'Segismundo', 'Segundo', 'Selena', 'Selene', 'Selina', 'Seneca', 'Septima', 'Septimio', 'Serafin', 'Serfina', 'Serafino', 'Serena', 'Serezade', 'Sergio', 'Seth', 'Severiano',
	'Shakira', 'Sheila', 'Shiva',
	'Sigfrido', 'Sigrid', 'Silvestre', 'Silvia', 'Silvio', 'Simba', 'Simbad', 'Simeon', 'Simon', 'Simplicio', 'Sinesio', 'Sinue', 'Siro', 'Sixto',
	'Socorro', 'Socrates', 'Sofia', 'Sofocles', 'Soledad', 'Sonia', 'Sonsoles', 'Soraya',
	'Susana',
	
	'Tadeo', 'Talia', 'Taliesin', 'Talon', 'Tamara', 'Tania', 'Tarik', 'Tarquinio', 'Tatiana',
	'Telemaco', 'Telma', 'Telmo', 'Teobaldo', 'Teodora', 'Teodorica', 'Teodorico', 'Teodoro', 'Teodosio', 'Teofilo', 'Teresa', 'Teseo',
	'Thais', 'Thiago', 'Thor',
	'Tiago', 'Tiberio', 'Tiburcio', 'Timon', 'Timotea', 'Timoteo', 'Tintoreto', 'Tirso', 'Tito', 'Tiziano',
	'Tlacoc', 'Tobias', 'Tolomeo', 'Tomas', 'Torcuato', 'Toribio',
	'Trajano',
	'Trinidad', 'Tristan', 'Triton',
	'Tubal', 'Tulio', 'Tupa', 'Tutankamon',
	
	'Ulises', 'Ulrico',
	'Umberta', 'Umberto',
	'Unai',
	'Urano', 'Urbano',
	'Ursula',
	
	'Vaiana', 'Valdemar', 'Valdo', 'Valente', 'Valentin', 'Valentina', 'Valentino', 'Valeria', 'Valerio', 'Vanesa',
	'Vega', 'Venecia', 'Ventura', 'Venus', 'Vercingetorix', 'Veronica', 'Vespasiano',
	'Vicenta', 'Vicente', 'Victor', 'Victoria', 'Viernes', 'Vilma', 'Vinicio', 'Violeta', 'Virgilio', 'Virginia', 'Viriato', 'Virtudes', 'Visnu', 'Vito', 'Vitorio', 'Viviana',
	'Vlad', 'Vladimir',
	'Vulcano',
	
	'Wally', 'Walter', 'Wamba', 'Wanda',
	'Wenceslao',
	'Wilfredo', 'Will', 'Witerica', 'Witerico',
	
	'Xander', 'Xavier',
	'Xena',
	'Ximena',
	
	'Yago', 'Yahve', 'Yasmin',
	'Yeray',
	'Ylenia',
	'Yocasta', 'Yolanda',
	'Yurena', 'Yuri',
	
	'Zacarias', 'Zafira', 'Zafiro', 'Zaira', 'Zara',
	'Zeferina', 'Zeferino', 'Zelda', 'Zenobia', 'Zenobio', 'Zenon', 'Zeus',
	'Zoe', 'Zoey', 'Zoilo', 'Zoraida', 'Zoser',
	'Zuleica', 'Zulema', 'Zuriñe'
	]
	
	index = randint(0, len(names) - 1)
	return names[index]

def get_random_surname():
	surnames = ['Abad', 'Abadias', 'Abalos', 'Abanto', 'Abascal', 'Abenia', 'Abril',
	'Acebes', 'Acebo', 'Acevedo', 'Acitores', 'Acosta',
	'Adanez',
	'Agostini', 'Agramonte', 'Aguado', 'Agudo', 'Aguero', 'Aguilar', 'Aguilera', 'Aguirre',
	'Alarcon', 'Alatriste', 'Alava', 'Alaves', 'Alba', 'Albacete', 'Albala', 'Albanchez', 'Albano', 'Albelda', 'Albeniz', 'Alberti', 'Albiol', 'Alcayde', 'Alcala', 'Alcalde', 'Alcantara', 'Alcañiz', 'Alcaraz', 'Alcazar', 'Alcobendas', 'Alcocer', 'Alcolado', 'Alcolea', 'Aldonza', 'Alexandre', 'Alfaro', 'Alkorta', 'Allende', 'Almagro', 'Almeida', 'Almodovar', 'Alonso', 'Altamira', 'Altolaguirre', 'Altozano', 'Alvarado', 'Alvarez', 'Alves',
	'Amado', 'Amador', 'Amaro', 'Amaya', 'Amenabar',
	'Anasagasti', 'Anderson', 'Anguita', 'Aniorte', 'Antunez',
	'Aparicio', 'Apostol',
	'Aquino',
	'Aragon', 'Aragones', 'Aramburu', 'Aramendi', 'Aranda', 'Arbeloa', 'Arcangel', 'Archuleta', 'Arenas', 'Arevalo', 'Arganda', 'Argoitia', 'Arguelles', 'Arguiñano', 'Arias',
	'Asenjo', 'Asensi', 'Asensio', 'Asturiano', 'Asturias', 
	'Austria',
	'Avalos', 'Avellan', 'Avila',
	'Ayuso',
	'Azaña', 'Aznar', 'Azores',
	
	""" ... """
	
	'Zabaleta', 'Zambrano', 'Zamora', 'Zamorano', 'Zapata', 'Zapatero', 'Zaplana', 'Zaragoza', 'Zaragozano', 'Zarate', 'Zarraga',
	'Zidane',
	'Zoco', 'Zoilo', 'Zorrilla',
	'Zubiri', 'Zubizarreta', 'Zugarramurdi', 'Zuñiga', 'Zurbaran', 'Zurdo', 'Zurutuza'
	]
	
	index = randint(0, len(surnames) - 1)
	return surnames[index]

def get_random_phone_number():
	phone_number = ""
	for i in range(9):
		number = randint(0,9)
		phone_number = phone_number + str(number)
	
	phones = Phone.objects.all()
	for phone in phones:
		if(phone_number == phone.number):
			phone_number = get_random_phone_number()
	
	return phone_number
	
def get_random_person():
	people = Person.objects.all()
	size = Person.objects.count()
	
	index = randint(0, size - 1)
	person = people[index]
	
	return person
	
def get_random_phone():
	phones = Phone.objects.all()
	size = Phone.objects.count()
	
	index = randint(0, size - 1)
	phone = phones[index]
	
	return phone
	
def get_random_place():
	places = ['Albacete', 'Alcala de Henares', 'Alicante', 'Almeria', 'Avila', 'Barcelona', 'Bilbao', 'Burgos', 'Caceres', 'Cadiz', 'Cartagena', 
			'Ceuta', 'Cordoba', 'Cuenca', 'Gerona', 'Gijon', 'Granada', 'Huelva', 'Jerez de la Frontera', 'La Coruña', 'Las Palmas', 'Leon', 
			'Lerida', 'Logroño', 'Lugo', 'Madrid', 'Malaga', 'Marbella', 'Melilla', 'Merida', 'Murcia', 'Oviedo', 'Palma de Mallorca', 
			'Pamplona', 'Puerto de Santa Maria', 'Santa Cruz de Tenerife', 'Santander', 'Santiago de Compostela', 'Sevilla', 'Segovia', 'Soria', 
			'Tarragona', 'Teruel', 'Toledo', 'Valencia', 'Valladolid', 'Vigo', 'Vitoria', 'Zaragoza'
			]
	
	index = randint(0, len(places) - 1)
	return places[index]

def get_random_date():
	date = ""
	
	year = randint(1900, 2019)
	month = randint(1, 12)
	if(month < 10):
		month = "0" + str(month)
	
	if(month == "02" or month == "04" or month == "06" or month == "09" or month == "11"):
		if(month == "02"):
			day = randint(1, 28)
		else:
			day = randint(1, 30)
	else:
		day = randint(1, 31)
	
	if(day < 10):
		day = "0" + str(day)
		
	date = str(day) + "-" + str(month) + "-" + str(year)
	return date

def get_random_time():
	time = ""
	
	hour = randint(0, 23)
	minute = randint(0, 59)
	
	time = str(hour) + ":" + str(minute)
	return time

def get_random_point():
	points = MeetingPoint.objects.all()
	size = MeetingPoint.objects.count()
	
	index = randint(0, size - 1)
	point = points[index]
	
	return point

def search_person_degree(node, people, phones, points, calls, meetings):
	dict = {}
	dict['people'] = []
	dict['phones'] = []
	dict['points'] = []
	dict['calls'] = []
	dict['meetings'] = []
	dict['ownerships'] = []
	dict['value'] = 0
	
	for person in people:
		if(person.id == node.id):
			dict['people'].append(person)
	
	for phone in phones:
		if(phone.owner.id == node.id):
			dict['phones'].append(phone)
			dict['ownerships'].append(phone)
			dict['value'] += 1
	
	for meeting in meetings:
		if(meeting.person.id == node.id):
			dict['meetings'].append(meeting)
			dict['points'].append(meeting.point)
			dict['value'] += 1
	
	return dict

def search_phone_degree(node, people, phones, points, calls, meetings):
	dict = {}
	dict['people'] = []
	dict['phones'] = []
	dict['points'] = []
	dict['calls'] = []
	dict['meetings'] = []
	dict['ownerships'] = []
	dict['value'] = 0
	
	for phone in phones:
		if(phone.number == node.number):
			dict['phones'].append(phone)
			dict['ownerships'].append(phone)
			dict['people'].append(phone.owner)
			dict['value'] += 1
	
	for call in calls:
		if(call.phone_1.number == node.number):
			dict['calls'].append(call)
			dict['phones'].append(call.phone_2)
			dict['value'] += 1
		if(call.phone_2.number == node.number):
			dict['calls'].append(call)
			dict['phones'].append(call.phone_1)
			dict['value'] += 1
	
	return dict

def search_point_degree(node, people, phones, points, calls, meetings):
	dict = {}
	dict['people'] = []
	dict['phones'] = []
	dict['points'] = []
	dict['calls'] = []
	dict['meetings'] = []
	dict['ownerships'] = []
	dict['value'] = 0
	
	for point in points:
		if(point.id == node.id):
			dict['points'].append(point)
	
	for meeting in meetings:
		if(meeting.point.id == node.id):
			dict['meetings'].append(meeting)
			dict['people'].append(meeting.person)
			dict['value'] += 1
	
	return dict

def search_degree(node, phones, calls, meetings):
	value = 0
	node_id = None
	node_type = str(node._meta.model)
	
	if(node_type == "<class 'apps.Nodes.models.Person'>" or node_type == "<class 'apps.Nodes.models.MeetingPoint'>"):
		node_id = node.id
	elif(node_type == "<class 'apps.Nodes.models.Phone'>"):
		node_id = node.number
	
	for phone in phones:
		if(phone.number == node_id):
			value += 1
		if(phone.owner.id == node_id):
			value += 1
			
	for meeting in meetings:
		if(meeting.person.id == node_id):
			value += 1
		if(meeting.point.id == node_id):
			value += 1
			
	for call in calls:
		if(call.phone_1.number == node_id):
			value += 1
		if(call.phone_2.number == node_id):
			value += 1
			
	return value

	
def search_graph_degree(people, phones, points, calls, meetings):
	dict = {}
	dict['people'] = []
	dict['phones'] = []
	dict['points'] = []
	max_value = 0
	for person in people:
		value = search_degree(person, phones, calls, meetings)
		dict['people'].append({'id':person.id, 'name':person.name, 'surname':person.surname, 'value':value})
		if(value > max_value):
			max_value = value
	for phone in phones:
		value = search_degree(phone, phones, calls, meetings)
		dict['phones'].append({'number':phone.number, 'owner':phone.owner, 'value':value})
		if(value > max_value):
			max_value = value
	for point in points:
		value = search_degree(point, phones, calls, meetings)
		dict['points'].append({'id':point.id, 'place':point.place, 'date':point.date, 'time':point.time, 'value':value})
		if(value > max_value):
			max_value = value
	
	dict['max_value'] = max_value
	return dict
	
def search_nxgraph_degree(people, phones, points, calls, meetings):
	G = get_graph(people, phones, points, calls, meetings)
	centrality = nx.degree_centrality(G)
	#print(centrality[node])
	dict = {}
	dict['people'] = []
	dict['phones'] = []
	dict['points'] = []
	max_value = 0
	for person in people:
		value = round(centrality[person], 2)
		dict['people'].append({'id':person.id, 'name':person.name, 'surname':person.surname, 'value':value})
		if(value > max_value):
			max_value = value
	for phone in phones:
		value = round(centrality[phone], 2)
		dict['phones'].append({'number':phone.number, 'owner':phone.owner, 'value':value})
		if(value > max_value):
			max_value = value
	for point in points:
		value = round(centrality[point], 2)
		dict['points'].append({'id':point.id, 'place':point.place, 'date':point.date, 'time':point.time, 'value':value})
		if(value > max_value):
			max_value = value
	
	dict['max_value'] = max_value
	return dict

def search_closeness(node, people, phones, points, calls, meetings):
	value = 0
	number_of_nodes = len(people) + len(phones) + len(points) - 1
	
	G = get_graph(people, phones, points, calls, meetings)
	
	for dest in G.nodes:
		if(node != dest):
			try:
				path = nx.shortest_path(G, source=node , target=dest)
			except nx.NetworkXNoPath:
				path = []
			value += len(path) - 1
	
	value = round((number_of_nodes / value), 2)
	return value

def search_graph_closeness(people, phones, points, calls, meetings):
	dict = {}
	dict['people'] = []
	dict['phones'] = []
	dict['points'] = []
	max_value = 0
	for person in people:
		value = search_closeness(person, people, phones, points, calls, meetings)
		dict['people'].append({'id':person.id, 'name':person.name, 'surname':person.surname, 'value':value})
		if(value > max_value):
			max_value = value
	for phone in phones:
		value = search_closeness(phone, people, phones, points, calls, meetings)
		dict['phones'].append({'number':phone.number, 'owner':phone.owner, 'value':value})
		if(value > max_value):
			max_value = value
	for point in points:
		value = search_closeness(point, people, phones, points, calls, meetings)
		dict['points'].append({'id':point.id, 'place':point.place, 'date':point.date, 'time':point.time, 'value':value})
		if(value > max_value):
			max_value = value
			
	dict['max_value'] = max_value
	return dict			
			

def search_nxgraph_closeness(people, phones, points, calls, meetings):
	G = get_graph(people, phones, points, calls, meetings)
	centrality = nx.closeness_centrality(G)
	#print(centrality[node])
	dict = {}
	dict['people'] = []
	dict['phones'] = []
	dict['points'] = []
	max_value = 0
	for person in people:
		value = round(centrality[person], 2)
		dict['people'].append({'id':person.id, 'name':person.name, 'surname':person.surname, 'value':value})
		if(value > max_value):
			max_value = value
	for phone in phones:
		value = round(centrality[phone], 2)
		dict['phones'].append({'number':phone.number, 'owner':phone.owner, 'value':value})
		if(value > max_value):
			max_value = value
	for point in points:
		value = round(centrality[point], 2)
		dict['points'].append({'id':point.id, 'place':point.place, 'date':point.date, 'time':point.time, 'value':value})
		if(value > max_value):
			max_value = value
	
	dict['max_value'] = max_value
	return dict
	
def search_betweeness(node, paths):
	betweeness_paths = []
	for path in paths:
		for i in range(len(path) - 2):
			if(path[i + 1] == node):
				betweeness_paths.append(path)
	
	value = len(betweeness_paths)
	return value
	
def search_graph_betweeness(people, phones, points, calls, meetings):
	dict = {}
	dict['people'] = []
	dict['phones'] = []
	dict['points'] = []
	max_value = 0
	paths = get_all_paths(people, phones, points, calls, meetings)
	for person in people:
		value = search_betweeness(person, paths)
		dict['people'].append({'id':person.id, 'name':person.name, 'surname':person.surname, 'value':value})
		if(value > max_value):
			max_value = value
	for phone in phones:
		value = search_betweeness(phone, paths)
		dict['phones'].append({'number':phone.number, 'owner':phone.owner, 'value':value})
		if(value > max_value):
			max_value = value
	for point in points:
		value = search_betweeness(point, paths)
		dict['points'].append({'id':point.id, 'place':point.place, 'date':point.date, 'time':point.time, 'value':value})
		if(value > max_value):
			max_value = value
	
	dict['max_value'] = max_value
	return dict
	
def search_nxgraph_betweeness(people, phones, points, calls, meetings):
	G = get_graph(people, phones, points, calls, meetings)
	centrality = nx.betweenness_centrality(G)
	#print(centrality[node])
	dict = {}
	dict['people'] = []
	dict['phones'] = []
	dict['points'] = []
	max_value = 0
	for person in people:
		value = round(centrality[person], 2)
		dict['people'].append({'id':person.id, 'name':person.name, 'surname':person.surname, 'value':value})
		if(value > max_value):
			max_value = value
	for phone in phones:
		value = round(centrality[phone], 2)
		dict['phones'].append({'number':phone.number, 'owner':phone.owner, 'value':value})
		if(value > max_value):
			max_value = value
	for point in points:
		value = round(centrality[point], 2)
		dict['points'].append({'id':point.id, 'place':point.place, 'date':point.date, 'time':point.time, 'value':value})
		if(value > max_value):
			max_value = value
	
	dict['max_value'] = max_value
	return dict
	
def search_eigenvector(node, people, phones, points, calls, meetings):
	all_degrees_sum = get_degrees_sum(people, phones, points, calls, meetings)
	all_eigenvalues_sum = get_eigenvalues_sum(all_degrees_sum, people, phones, points, calls, meetings)
	
	sum = 0
	for call in calls:
		if(call.phone_1 == node):
			sum += get_eigenvalue(call.phone_2, all_degrees_sum, people, phones, points, calls, meetings)
		if(call.phone_2 == node):
			sum += get_eigenvalue(call.phone_1, all_degrees_sum, people, phones, points, calls, meetings)
			
	for meeting in meetings:
		if(meeting.person == node):
			sum += get_eigenvalue(meeting.point, all_degrees_sum, people, phones, points, calls, meetings)
		if(meeting.point == node):
			sum += get_eigenvalue(meeting.person, all_degrees_sum, people, phones, points, calls, meetings)
			
	for phone in phones:
		if(phone.owner == node):
			sum += get_eigenvalue(phone, all_degrees_sum, people, phones, points, calls, meetings)
		if(phone == node):
			sum += get_eigenvalue(phone.owner, all_degrees_sum, people, phones, points, calls, meetings)
	
	value = round((sum / all_eigenvalues_sum), 2)	
	return value
	
def search_graph_eigenvector(people, phones, points, calls, meetings):
	dict = {}
	dict['people'] = []
	dict['phones'] = []
	dict['points'] = []
	max_value = 0
	for person in people:
		value = search_eigenvector(person, people, phones, points, calls, meetings)
		dict['people'].append({'id':person.id, 'name':person.name, 'surname':person.surname, 'value':value})
		if(value > max_value):
			max_value = value
	for phone in phones:
		value = search_eigenvector(phone, people, phones, points, calls, meetings)
		dict['phones'].append({'number':phone.number, 'owner':phone.owner, 'value':value})
		if(value > max_value):
			max_value = value
	for point in points:
		value = search_eigenvector(point, people, phones, points, calls, meetings)
		dict['points'].append({'id':point.id, 'place':point.place, 'date':point.date, 'time':point.time, 'value':value})
		if(value > max_value):
			max_value = value
	
	dict['max_value'] = max_value
	return dict

def search_nxgraph_eigenvector(people, phones, points, calls, meetings):
	G = get_graph(people, phones, points, calls, meetings)
	centrality = nx.eigenvector_centrality(G)
	#print(centrality[node])
	dict = {}
	dict['people'] = []
	dict['phones'] = []
	dict['points'] = []
	max_value = 0
	for person in people:
		value = round(centrality[person], 2)
		dict['people'].append({'id':person.id, 'name':person.name, 'surname':person.surname, 'value':value})
		if(value > max_value):
			max_value = value
	for phone in phones:
		value = round(centrality[phone], 2)
		dict['phones'].append({'number':phone.number, 'owner':phone.owner, 'value':value})
		if(value > max_value):
			max_value = value
	for point in points:
		value = round(centrality[point], 2)
		dict['points'].append({'id':point.id, 'place':point.place, 'date':point.date, 'time':point.time, 'value':value})
		if(value > max_value):
			max_value = value
	
	dict['max_value'] = max_value
	return dict
	
def search_harmonic_centrality(node, people, phones, points, calls, meetings):
	value = 0
	number_of_nodes = len(people) + len(phones) + len(points) - 1
	
	G = get_graph(people, phones, points, calls, meetings)
	
	for dest in G.nodes:
		if(node != dest):
			try:
				path = nx.shortest_path(G, source=node , target=dest)
			except nx.NetworkXNoPath:
				path = []
			if(len(path) > 1):
				value += 1 / (len(path) - 1)
	
	value = round(value / number_of_nodes, 2)
	return value
	
def search_graph_harmony(people, phones, points, calls, meetings):
	dict = {}
	dict['people'] = []
	dict['phones'] = []
	dict['points'] = []
	max_value = 0
	for person in people:
		value = search_harmonic_centrality(person, people, phones, points, calls, meetings)
		dict['people'].append({'id':person.id, 'name':person.name, 'surname':person.surname, 'value':value})
		if(value > max_value):
			max_value = value
	for phone in phones:
		value = search_harmonic_centrality(phone, people, phones, points, calls, meetings)
		dict['phones'].append({'number':phone.number, 'owner':phone.owner, 'value':value})
		if(value > max_value):
			max_value = value
	for point in points:
		value = search_harmonic_centrality(point, people, phones, points, calls, meetings)
		dict['points'].append({'id':point.id, 'place':point.place, 'date':point.date, 'time':point.time, 'value':value})
		if(value > max_value):
			max_value = value
			
	dict['max_value'] = max_value
	return dict
	
def search_katz_centrality(node, people, phones, points, calls, meetings):
	nodes_by_distance = {}
	max_len = 0
	
	G = get_graph(people, phones, points, calls, meetings)
	
	for dest in G.nodes:
		if(node != dest):
			try:
				path = nx.shortest_path(G, source=node , target=dest)
				if((len(path) - 1) > max_len):
					max_len = len(path) - 1
			except nx.NetworkXNoPath:
				path = []
			if(nodes_by_distance.get(str(len(path) - 1)) == None):
				nodes_by_distance[str(len(path) - 1)] = []
			nodes_by_distance[str(len(path) - 1)].append(dest)
	
	alfa = 0.5
	value = 0
	for i in range(max_len):
		if(nodes_by_distance.get(str(i)) != None):
			value += math.pow(alfa, i) * len(nodes_by_distance[str(i)])
			#print(math.pow(alfa, i) * len(nodes_by_distance[str(i)]))
			#print(nodes_by_distance[str(i)])
		
	value = round(value, 2)
	return value
	
def search_graph_katz(people, phones, points, calls, meetings):
	dict = {}
	dict['people'] = []
	dict['phones'] = []
	dict['points'] = []
	max_value = 0
	
	for person in people:
		value = search_katz_centrality(person, people, phones, points, calls, meetings)
		dict['people'].append({'id':person.id, 'name':person.name, 'surname':person.surname, 'value':value})
		if(value > max_value):
			max_value = value
	for phone in phones:
		value = search_katz_centrality(phone, people, phones, points, calls, meetings)
		dict['phones'].append({'number':phone.number, 'owner':phone.owner, 'value':value})
		if(value > max_value):
			max_value = value
	for point in points:
		value = search_katz_centrality(point, people, phones, points, calls, meetings)
		dict['points'].append({'id':point.id, 'place':point.place, 'date':point.date, 'time':point.time, 'value':value})
		if(value > max_value):
			max_value = value
	
	dict['max_value'] = max_value
	return dict
	
def search_nxgraph_katz(people, phones, points, calls, meetings):
	G = get_graph(people, phones, points, calls, meetings)
	centrality = nx.katz_centrality(G)
	#print(centrality[node])
	dict = {}
	dict['people'] = []
	dict['phones'] = []
	dict['points'] = []
	max_value = 0
	for person in people:
		value = round(centrality[person], 2)
		dict['people'].append({'id':person.id, 'name':person.name, 'surname':person.surname, 'value':value})
		if(value > max_value):
			max_value = value
	for phone in phones:
		value = round(centrality[phone], 2)
		dict['phones'].append({'number':phone.number, 'owner':phone.owner, 'value':value})
		if(value > max_value):
			max_value = value
	for point in points:
		value = round(centrality[point], 2)
		dict['points'].append({'id':point.id, 'place':point.place, 'date':point.date, 'time':point.time, 'value':value})
		if(value > max_value):
			max_value = value
	
	dict['max_value'] = max_value
	return dict
	
def get_graph(people, phones, points, calls, meetings):
	G = nx.Graph()
	
	for p in people:
		G.add_node(p)
	for p in phones:
		G.add_node(p)
	for p in points:
		G.add_node(p)
		
	for l in calls:
		G.add_edge(l.phone_1, l.phone_2)
	for l in meetings:
		G.add_edge(l.person, l.point)
	for l in phones:
		G.add_edge(l, l.owner)
	
	return G		
			
	
def add_nodes_of_path(path, dict, calls, meetings, phones):
	for i in range(len(path)):
		if(str(path[i]._meta.model) == "<class 'apps.Nodes.models.Person'>"):
			dict['people'].append(path[i])
			if(i > 0):
				if(str(path[i-1]._meta.model) == "<class 'apps.Nodes.models.MeetingPoint'>"):
					for meeting in meetings:
						if(meeting.person == path[i] and meeting.point == path[i-1]):
							dict['meetings'].append(meeting)
				elif(str(path[i-1]._meta.model) == "<class 'apps.Nodes.models.Phone'>"):
					for phone in phones:
						if(phone.owner == path[i] and phone == path[i-1]):
							dict['ownerships'].append(phone)
		elif(str(path[i]._meta.model) == "<class 'apps.Nodes.models.Phone'>"):
			dict['phones'].append(path[i])
			if(i > 0):
				if(str(path[i-1]._meta.model) == "<class 'apps.Nodes.models.Phone'>"):
					for call in calls:
						if(call.phone_1 == path[i] and call.phone_2 == path[i-1]):
							dict['calls'].append(call)
						elif(call.phone_2 == path[i] and call.phone_1 == path[i-1]):
							dict['calls'].append(call)
				elif(str(path[i-1]._meta.model) == "<class 'apps.Nodes.models.Person'>"):
					for phone in phones:
						if(phone == path[i] and phone.owner == path[i-1]):
							dict['ownerships'].append(phone)
		elif(str(path[i]._meta.model) == "<class 'apps.Nodes.models.MeetingPoint'>"):
			dict['points'].append(path[i])
			if(i > 0):
				if(str(path[i-1]._meta.model) == "<class 'apps.Nodes.models.Person'>"):
					for meeting in meetings:
						if(meeting.point == path[i] and meeting.person == path[i-1]):
							dict['meetings'].append(meeting)

def get_all_paths(people, phones, points, calls, meetings):
	G = get_graph(people, phones, points, calls, meetings)
	paths = []
	
	get_all_paths_between_models(G, paths, people, people)
	get_all_paths_between_models(G, paths, people, phones)
	get_all_paths_between_models(G, paths, people, points)
	
	get_all_paths_between_models(G, paths, phones, phones)
	get_all_paths_between_models(G, paths, phones, people)
	get_all_paths_between_models(G, paths, phones, points)
	
	get_all_paths_between_models(G, paths, points, points)
	get_all_paths_between_models(G, paths, points, people)
	get_all_paths_between_models(G, paths, points, phones)
	
	return paths
	
def get_all_paths_between_models(G, paths, nodes_type1, nodes_type2):
	for p1 in nodes_type1:
		for p2 in nodes_type2:
			if(p1 != p2):
				try:
					path = nx.shortest_path(G, source=p1 , target=p2)
				except nx.NetworkXNoPath:
					path = []
				if(len(path) > 0):
					paths.append(path)					
	
def get_degrees_sum(people, phones, points, calls, meetings):
	sum = 0
	
	for person in people:
		value = search_degree(person, phones, calls, meetings)
		sum += value
	for phone in phones:
		value = search_degree(phone, phones, calls, meetings)
		sum += value
	for point in points:
		value = search_degree(point, phones, calls, meetings)
		sum += value
	
	return sum
	
def get_eigenvalues_sum(all_degrees_sum, people, phones, points, calls, meetings):
	sum = 0
	
	for person in people:
		eigenvalue = get_eigenvalue(person, all_degrees_sum, people, phones, points, calls, meetings)
		sum += eigenvalue
	for phone in phones:
		eigenvalue = get_eigenvalue(phone, all_degrees_sum, people, phones, points, calls, meetings)
		sum += eigenvalue
	for point in points:
		eigenvalue = get_eigenvalue(point, all_degrees_sum, people, phones, points, calls, meetings)
		sum += eigenvalue
	
	return sum
	
def get_eigenvalue(node, all_degrees_value, people, phones, points, calls, meetings):
	type_node = str(node._meta.model)
	
	dict = {}
	if(type_node == "<class 'apps.Nodes.models.Person'>"):
		dict = search_person_degree(node, people, phones, points, calls, meetings)
	if(type_node == "<class 'apps.Nodes.models.Phone'>"):
		dict = search_phone_degree(node, people, phones, points, calls, meetings)
	if(type_node == "<class 'apps.Nodes.models.MeetingPoint'>"):
		dict = search_point_degree(node, people, phones, points, calls, meetings)
	
	sum = 0
	for person in dict['people']:
		if(person != node):
			d = search_person_degree(person, people, phones, points, calls, meetings)
			sum += d['value']
	for phone in dict['phones']:
		if(phone != node):
			d = search_phone_degree(phone, people, phones, points, calls, meetings)
			sum += d['value']
	for point in dict['points']:
		if(point != node):
			d = search_point_degree(point, people, phones, points, calls, meetings)
			sum += d['value']
	
	eigenvalue = round((sum / all_degrees_value), 2)
	return eigenvalue
	
def quit_repeat_items(dict):
	for key in dict.keys():
		if(type(dict[key]) is list):
			auxList = []
			for item in dict[key]:
				insert = True
				for auxItem in auxList:
					if(auxItem == item):
						insert = False
				if(insert == True):
					auxList.append(item)
			dict[key] = auxList
	
	return dict
	
def get_model_object_by_id(pk):
	try:
		obj = Person.objects.get(id=pk)
	except:
		try:
			obj = Phone.objects.get(number=pk)
		except:
			obj = MeetingPoint.objects.get(id=pk)
	
	return obj
	
"""
def get_links(phones, calls, meetings):
	links = []
	for phone in phones:
		link = {}
		link["source"] = phone
		link["dest"] = phone.owner
		link["type"] = "ownership"
		links.append(link)
	for call in  calls:
		link = {}
		link["source"] = call.phone_1
		link["dest"] = call.phone_2
		link["type"] = "call"
		links.append(link)
	for meeting in meetings:
		link = {}
		link["source"] = meeting.person
		link["dest"] = meeting.point
		link["type"] = "meeting"
		links.append(link)
	
	return links

def get_linked_nodes(node, links):
	linked_nodes = []
	
	for i in range(len(links)):
		source = links[i]["source"]
		dest = links[i]["dest"]
		if(source == node):
			linked_nodes.append(dest)
		elif(dest == node):
			linked_nodes.append(source)
			
	return linked_nodes
	

def search_path(source, dest, links, path, cola, pozo, firstSource):
	#print("SOURCE")
	#print(source)
	pozo.append(source)
	if (len(cola) > 0):
		del cola[0]
	
	#Mirar nodos conectados al nodo dado
	linked_nodes = get_linked_nodes(source, links)
	terminado = False
	
	for i in range(len(linked_nodes)):
		#print("ITERACION " + str(i))
		#print(linked_nodes[i])
		#print(dest)
		if (linked_nodes[i] == dest):
			path.append(dest)
			if (source != firstSource):
				cola.clear()
				pozo.clear()
				search_path(firstSource, source, links, path, cola, pozo, firstSource)
			else:
				path.append(firstSource)
			terminado = True
			#print("PATH")
			#print(path)
		else:
			#Guardar en una cola los nodos conectados
			insert = True
			for j in range(len(cola)):
				if (cola[j] == linked_nodes[i]):
					insert = False
			for j in range(len(pozo)):
				if (pozo[j] == linked_nodes[i]):
					insert = False
			
			if (insert):
				cola.append(linked_nodes[i])
	
	if (terminado == False):
		#print("COLA")
		#print(cola)
		max = Person.objects.count() + Phone.objects.count() + MeetingPoint.objects.count()
		if(len(cola) > 0): 
			search_path(cola[0], dest, links, path, cola, pozo, firstSource)
		#else:
			#print("No existe camino entre " + str(firstSource) + " y " + str(dest))
"""
