from django.urls import re_path
from apps.Graphs.views import GraphList, GraphCreate

urlpatterns = [
	re_path(r'^newGraph$', GraphCreate.as_view(), name='newGraph'),
	re_path(r'^listGraph$', GraphList.as_view(), name='listGraph'),
]