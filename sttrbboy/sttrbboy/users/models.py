# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from sttrbboy import settings


class Profile(models.Model):
	name = models.CharField(max_length=128)
	gender_pronouns = models.CharField(max_length=128)
	#phone_number = PhoneNumberField(blank=True)
	user = models.OneToOneField(settings.AUTH_USER_MODEL)