# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from localflavor.us.models import PhoneNumberField

from sttrbboy.hunt.models import *

# Create your models here.
class Scavvie(models.Model):
	class Meta:
		unique_together = (('user', 'hunt'))

	page_captain = models.BooleanField(default=False)
	captain = models.BooleanField(default=False)


class Profile(models.Model):
	name = models.CharField(max_length=128)
	gender_pronouns = models.CharField(max_length=128)
	phone_number = PhoneNumberField(blank=True)