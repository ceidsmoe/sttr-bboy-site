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

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('email', 'phone number')

    agree = forms.BooleanField()

    def __init__(self, *args, **kwargs):
        self.hunt = kwargs.pop('hunt')
        super(RegistrationForm, self).__init__(*args, **kwargs)


def validate_phone_number(phone_str):
    phone_str = phone_str.replace(".", "").replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
    if phone_str[0] == "1":
        phone_str = phone_str[1:]
    if len(phone_str) != 10:
        raise ValidationError('Invalid Phone Number')
