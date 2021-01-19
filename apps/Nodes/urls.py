from django.urls import re_path
from apps.Nodes.views import PersonList

urlpatterns = [
	re_path(r'^listPerson$', PersonList.as_view(), name='listPerson'),
]