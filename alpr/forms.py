from django import forms
from .models import Alpr


class AlprForm(forms.Form):

    image = forms.ImageField()

	# class Meta:
	# 	model = Alpr
	# 	fields = ['image']