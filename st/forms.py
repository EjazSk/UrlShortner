from django import forms
from .models import Shortner
from django.forms import ModelForm, TextInput

class ShortnerForm(forms.ModelForm):
	class Meta:
		model  = Shortner
		fields = ['url_field',]
		widgets = {
 		'url_field': TextInput(attrs={'type': 'text','class':'form-control','placeholder':'Enter Your Url','label':'Enter'}),
		}


