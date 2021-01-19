from django import forms

from apps.Nodes.models import Person, Phone, MeetingPoint

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

class PhoneForm(forms.ModelForm):
	
	class Meta:
		model = Phone
		fields = [
			'number',
			'owner',
		]
		labels = {
			'number': 'Number',
			'owner': 'Owner'
		}
		widgets = {
			'number': forms.TextInput(attrs={'class':'form-control'}),
			'owner': forms.Select(attrs={'class':'form-control'}),
		}

class MeetingPointForm(forms.ModelForm):
	
	class Meta:
		model = MeetingPoint
		fields = [
			'id',
			'place',
			'date',
			'time',
		]
		labels = {
			'id': 'Id',
			'place': 'Place',
			'date': 'Date',
			'time': 'Time'
		}
		widgets = {
			'id': forms.TextInput(attrs={'class':'form-control'}),
			'place': forms.TextInput(attrs={'class':'form-control'}),
			'date': forms.TextInput(attrs={'class':'form-control'}),
			'time': forms.TextInput(attrs={'class':'form-control'}),
		}
