from rest_framework.serializers import ModelSerializer

from apps.Nodes.models import Person, Phone, MeetingPoint

class PersonSerializer(ModelSerializer):
	
	class Meta:
		model = Person
		fields = ('id', 'name', 'surname')

class PhoneSerializer(ModelSerializer):
	
	class Meta:
		model = Phone
		fields = ('number', 'owner')

class MeetingPointSerializer(ModelSerializer):
	
	class Meta:
		model = MeetingPoint
		fields = ('id', 'place', 'date', 'time')