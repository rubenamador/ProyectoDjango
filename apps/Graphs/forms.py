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

from apps.Nodes.models import Phone

class PersonForm(forms.ModelForm):
	
	class Meta:
		model = Phone
		fields = [
			'owner',
		]
		labels = {
			'owner': 'Owner'
		}
		widgets = {
			'owner': forms.Select(attrs={'class':'form-control'}),
		}

from apps.Links.models import Call

class PhoneForm(forms.ModelForm):
	
	class Meta:
		model = Call
		fields = [
			'phone_1',
		]
		labels = {
			'phone_1': 'Phone_1'
		}
		widgets = {
			'phone_1': forms.Select(attrs={'class':'form-control'}),
		}

from apps.Links.models import Meeting

class MeetingPointForm(forms.ModelForm):
	
	class Meta:
		model = Meeting
		fields = [
			'point',
		]
		labels = {
			'point': 'Point'
		}
		widgets = {
			'point': forms.Select(attrs={'class':'form-control'}),
		}
