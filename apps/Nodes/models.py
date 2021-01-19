from django.db import models

# Create your models here.

class Person(models.Model):
	id = models.CharField(max_length=25, primary_key=True)
	name = models.CharField(max_length=25, default='')
	surname = models.CharField(max_length=25, default='')
	
	class Meta:
		ordering = ['name']
		
	def __str__(self):
		return '{}'.format(self.id)

class Phone(models.Model):
	number = models.CharField(max_length=9, primary_key=True)
	owner = models.ForeignKey(Person, null=True, blank=True, on_delete=models.CASCADE)
	
	class Meta:
		ordering = ['number']
		
	def __str__(self):
		return '{}'.format(self.number)

class MeetingPoint(models.Model):
	id = models.CharField(max_length=25, primary_key=True)
	place = models.CharField(max_length=25, default='')
	date = models.CharField(max_length=10, default='')
	time = models.CharField(max_length=5, default='')

	class Meta:
		ordering = ['id']
		
	def __str__(self):
		return '{}'.format(self.id)
