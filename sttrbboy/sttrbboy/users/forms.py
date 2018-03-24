from django import forms
from django.contrib.auth.models import User

from sttrbboy.users.models import *

class UserRegistrationForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password')

	def __init__(self, *args, **kwargs):
		super(UserRegistrationForm, self).__init__(*args, **kwargs)
		self.fields['username'].help_text = "Enter a username."
		self.fields['first_name'].help_text = "Enter your first name."
		self.fields['last_name'].help_text = "Enter your last name."
		self.fields['email'].help_text = "Enter your email address."
		self.fields['password'].help_text = "Enter a password."
		self.fields['password'].widget = forms.PasswordInput()

	def clean(self):
		data = super(UserRegistrationForm, self).clean()
		username = data.get('username')
		first_name = data.get('first_name')
		last_name = data.get('last_name')
		email = data.get('email')
		password = data.get('password')

		if not(username and first_name and last_name and email and password):
			self.error_class(['Please fill out all of the fields.'])
		try:
			User.objects.get(username=username)
			self.error_class(['Someone already has that username.'])
		except User.DoesNotExist:
			pass
		return data


class ProfileForm(forms.ModelForm):

	class Meta:
		model = Profile
		exclude = ('user',)

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user')
		super(ProfileForm, self).__init__(*args, **kwargs)
