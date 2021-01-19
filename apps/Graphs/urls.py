from django.urls import re_path
from apps.Graphs.views import GraphList

urlpatterns = [
	re_path(r'^listGraph$', GraphList.as_view(), name='listGraph'),
]