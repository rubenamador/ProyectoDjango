from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from rest_framework.views import APIView

from apps.Graphs.forms import GraphForm
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
