from django import forms
from .models import Shortner
class ShortnerForm(forms.ModelForm):
	class Meta:
		model  = Shortner
		fields = ['url_field',]