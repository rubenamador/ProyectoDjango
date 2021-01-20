from django.urls import re_path
from apps.Graphs.views import GraphList, GraphCreate, GraphUpdate, GraphDelete, GraphAPI
from apps.Graphs.views import all_graphs_delete

urlpatterns = [
	re_path(r'^newGraph$', GraphCreate.as_view(), name='newGraph'),
	re_path(r'^listGraph$', GraphList.as_view(), name='listGraph'),
	re_path(r'^editGraph/(?P<pk>[\w|\W]+)/$', GraphUpdate.as_view(), name='editGraph'),
	re_path(r'^deleteGraph/(?P<pk>[\w|\W]+)/$', GraphDelete.as_view(), name='deleteGraph'),
	re_path(r'^deleteAllGraphs$', all_graphs_delete, name='deleteAllGraphs'),
	re_path(r'^apiGraph$', GraphAPI.as_view(), name='apiGraph'),
]