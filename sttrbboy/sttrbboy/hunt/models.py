# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from sttrbboy.users import *


def gen_rules_filename(instance, fn):
	return "lists/%s%s" % (instance.name, os.path.splitext(fn)[1])

# Create your models here.
class Hunt(models.Model):
	year = models.IntegerField()
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	list_pdf = models.FileField(upload_to=gen_list_filename, storage=OverwriteFileSystemStorage())

	def __unicode__(self):
		return self.name

class Item(models.Model):
	number = models.IntegerField(unique=True)
	points = models.DecimalField(max_digits=8, decimal_places=5)
	short_desc = models.CharField(max_length=128)
	full_desc = TextField(blank=True)
	completed = models.BooleanField(default=False)
	started = models.BooleanField(defaul=False)

	hunt = models.ForeignKey(Hunt, related_name='items')
	page_captain = models.ForeignKey(Scavvie, related_name='page_items')
	interested_scavvies = models.ManyToManyField(Scavvie, related_name='interested_items')
	completed_scavvies = models.ManyToManyField(Scavvie, related_name='completed_items')


class Comment(models.Model):
	text = models.CharField(max_length=512)
	item = models.ForeignKey(Item, related_name='comments')