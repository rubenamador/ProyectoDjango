from django.urls import re_path
from apps.Graphs.views import GraphList, GraphCreate, GraphUpdate

urlpatterns = [
	re_path(r'^newGraph$', GraphCreate.as_view(), name='newGraph'),
	re_path(r'^listGraph$', GraphList.as_view(), name='listGraph'),
	re_path(r'^editGraph/(?P<pk>[\w|\W]+)/$', GraphUpdate.as_view(), name='editGraph'),
]