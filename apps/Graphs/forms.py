from django import forms

from apps.Graphs.models import Graph

class GraphForm(forms.ModelForm):
	
	class Meta:
		model = Graph
		fields = [
			'id',
		]
		labels = {
			'id' : 'Id',
		}
		widgets = {
			'id': forms.TextInput(attrs={'class':'form-control'}),
		}