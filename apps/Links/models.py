from django.db import models

from apps.Nodes.models import Person, Phone, MeetingPoint

# Create your models here.

class Call(models.Model):
	id = models.CharField(max_length=25, primary_key=True)
	phone_1 = models.OneToOneField(Phone, related_name="phone_1+", null=True, blank=True, on_delete=models.CASCADE)
	phone_2 = models.OneToOneField(Phone, related_name="phone_2+", null=True, blank=True, on_delete=models.CASCADE)
	
	class Meta:
		ordering = ['id']
		
	def __str__(self):
		return '{}'.format(self.id)

class Meeting(models.Model):
	id = models.CharField(max_length=25, primary_key=True)
	person = models.OneToOneField(Person, related_name="person+", null=True, blank=True, on_delete=models.CASCADE)
	point = models.OneToOneField(MeetingPoint, related_name="point+", null=True, blank=True, on_delete=models.CASCADE)
	
	class Meta:
		ordering = ['id']
		
	def __str__(self):
		return '{}'.format(self.id)
