from django import forms

from apps.Nodes.models import Person

class PersonForm(forms.ModelForm):
	
	class Meta:
		model = Person
		fields = [
			'id',
			'name',
			'surname',
		]
		labels = {
			'id': 'Id',
			'name': 'Name',
			'surname': 'Surname'
		}
		widgets = {
			'id': forms.TextInput(attrs={'class':'form-control'}),
			'name': forms.TextInput(attrs={'class':'form-control'}),
			'surname': forms.TextInput(attrs={'class':'form-control'}),
		}
