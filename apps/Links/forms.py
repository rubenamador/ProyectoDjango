from django import forms

from apps.Links.models import Call, Meeting

class CallForm(forms.ModelForm):
	
	class Meta:
		model = Call
		fields = [
			'id',
			'phone_1',
			'phone_2',
		]
		labels = {
			'id' : 'Id',
			'phone_1': 'Phone_1',
			'phone_2': 'Phone_2'
		}
		widgets = {
			'id': forms.TextInput(attrs={'class':'form-control'}),
			'phone_1': forms.Select(attrs={'class':'form-control'}),
			'phone_2': forms.Select(attrs={'class':'form-control'}),
		}

class MeetingForm(forms.ModelForm):
	
	class Meta:
		model = Meeting
		fields = [
			'id',
			'person',
			'point',
		]
		labels = {
			'id': 'Id',
			'person': 'Person',
			'point': 'Point'
		}
		widgets = {
			'id': forms.TextInput(attrs={'class':'form-control'}),
			'person': forms.Select(attrs={'class':'form-control'}),
			'point': forms.Select(attrs={'class':'form-control'}),
		}
