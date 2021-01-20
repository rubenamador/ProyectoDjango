from django.urls import re_path
from apps.Graphs.views import GraphList, GraphCreate, GraphUpdate, GraphDelete, GraphAPI
from apps.Graphs.views import all_graphs_delete
from apps.Graphs.views import GraphView
from apps.Graphs.views import random_graph_create
from apps.Graphs.views import DegreeForm, DegreePersonView, DegreePhoneView, DegreeMeetingPointView
from apps.Graphs.views import DegreeGraph
from apps.Graphs.views import PathForm, PathView
from apps.Graphs.views import ClosenessGraph

urlpatterns = [
	re_path(r'^newGraph$', GraphCreate.as_view(), name='newGraph'),
	re_path(r'^listGraph$', GraphList.as_view(), name='listGraph'),
	re_path(r'^editGraph/(?P<pk>[\w|\W]+)/$', GraphUpdate.as_view(), name='editGraph'),
	re_path(r'^deleteGraph/(?P<pk>[\w|\W]+)/$', GraphDelete.as_view(), name='deleteGraph'),
	re_path(r'^deleteAllGraphs$', all_graphs_delete, name='deleteAllGraphs'),
	re_path(r'^apiGraph$', GraphAPI.as_view(), name='apiGraph'),
	re_path(r'^viewGraph/(?P<pk>[\w|\W]+)/$', GraphView.as_view(), name='viewGraph'),
	re_path(r'^createRandomGraph$', random_graph_create, name='createRandomGraph'),
	re_path(r'^formDegree/(?P<pk>[\w|\W]+)/$', DegreeForm.as_view(), name='formDegree'),
	re_path(r'^viewDegreePerson/(?P<pk>[\w|\W]+)/(?P<pk2>[\w|\W]+)/$', DegreePersonView.as_view(), name='viewDegreePerson'),
	re_path(r'^viewDegreePhone/(?P<pk>[\w|\W]+)/(?P<pk2>[\w|\W]+)/$', DegreePhoneView.as_view(), name='viewDegreePhone'),
	re_path(r'^viewDegreeMeetingPoint/(?P<pk>[\w|\W]+)/(?P<pk2>[\w|\W]+)/$', DegreeMeetingPointView.as_view(), name='viewDegreeMeetingPoint'),
	re_path(r'^graphDegree/(?P<pk>[\w|\W]+)/$', DegreeGraph.as_view(), name='graphDegree'),
	re_path(r'^formPath/(?P<pk>[\w|\W]+)/$', PathForm.as_view(), name='formPath'),
	re_path(r'^viewPath/(?P<pk>[\w|\W]+)/(?P<pk2>[\w|\W]+)/(?P<pk3>[\w|\W]+)/$', PathView.as_view(), name='viewPath'),
	re_path(r'^graphCloseness/(?P<pk>[\w|\W]+)/$', ClosenessGraph.as_view(), name='graphCloseness'),
]