from django import forms
from .models import Link

class LinkForm(forms.ModelForm):
	class Meta:
		model = Link
		fields = [
			'url',
			'tags',
		]
		widgets = {
			'url': forms.TextInput(attrs={'class':'ui input'}),
			'tags': forms.TextInput(attrs={'class':'ui form'}),
		}