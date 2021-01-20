from rest_framework.serializers import ModelSerializer

from apps.Graphs.models import Graph

class GraphSerializer(ModelSerializer):
	
	class Meta:
		model = Graph
		fields = '__all__'