from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.admin.widgets import FilteredSelectMultiple

from sttrbboy.hunt.models import *

class HuntRegistrationForm(forms.ModelForm):
	class Meta:
		model = Scavvie
		fields = ('page_captain',)

	def __init__(self, *args, **kwargs):
		self.hunt = kwargs.pop('hunt')
		super(HuntRegistrationForm, self).__init__(*args, **kwargs)
