from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.admin.widgets import FilteredSelectMultiple

from sttrbboy.hunt.models import *

class ItemForm(forms.Form):
	interest = forms.BooleanField(initial=False, required=False)
	work = forms.BooleanField(initial=False, required=False)
	complete = forms.BooleanField(initial=False, required=False)

	def __init__(self, *args, **kwargs):
		del kwargs['instance']
		super(ItemForm, self).__init__(*args, **kwargs)

	def clean(self):
		data = super(ItemForm, self).clean()
		self.interested = data.get('interest', '')
		self.working = data.get('work', '')
		self.completed = data.get('complete', '')
		return data


class ItemCommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('text',)