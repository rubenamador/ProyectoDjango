from rest_framework.serializers import ModelSerializer

from apps.Links.models import Call, Meeting

class CallSerializer(ModelSerializer):
	
	class Meta:
		model = Call
		fields = ('id', 'phone_1', 'phone_2')
		
class MeetingSerializer(ModelSerializer):
	
	class Meta:
		model = Meeting
		fields = ('id', 'person', 'point')