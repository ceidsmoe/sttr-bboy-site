# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

from sttrbboy import settings


class Profile(models.Model):
	name = models.CharField(max_length=128)
	gender_pronouns = models.CharField(max_length=128)
	phone_number = PhoneNumberField(blank=True, default='')
	user = models.OneToOneField(settings.AUTH_USER_MODEL)

	@models.permalink
	def get_absolute_url(self):
		return ("users|account",)

	def __unicode__(self):
		if self.name:
			return self.name
		else:
			return self.user.first_name + " " + self.user.last_name

def get_or_create_profile(sender, **kwargs):
	if not kwargs.get('raw'):
		profile, created = Profile.objects.get_or_create(user=kwargs['instance'])

models.signals.post_save.connect(get_or_create_profile, sender=User)