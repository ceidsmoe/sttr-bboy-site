# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from sttrbboy import settings


class Profile(models.Model):
	name = models.CharField(max_length=128)
	gender_pronouns = models.CharField(max_length=128)
	#phone_number = PhoneNumberField(blank=True)
	user = models.OneToOneField(settings.AUTH_USER_MODEL)

def get_or_create_profile(sender, **kwargs):
	if not kwargs.get('raw'):
		profile, created = Profile.objects.get_or_create(user=kwargs['instance'])

models.signals.post_save.connect(get_or_create_profile, sender=User)