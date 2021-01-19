from django.db import models

from apps.Nodes.models import Person, Phone
from apps.Links.models import Call, Meeting

# Create your models here.

class Graph(models.Model):
	id = models.CharField(max_length=25, primary_key=True)
	
	class Meta:
		ordering = ['id']
	
	def __str__(self):
		return '{}'.format(self.id)
