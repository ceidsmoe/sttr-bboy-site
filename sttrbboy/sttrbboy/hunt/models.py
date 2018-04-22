# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.db import models
from django.utils import timezone

from sttrbboy.overwrite_fs import OverwriteFileSystemStorage
from sttrbboy import settings


def gen_list_filename(instance, fn):
        return "lists/%d%s" % (instance.year, os.path.splitext(fn)[1])


# Create your models here.
class Hunt(models.Model):
        year = models.IntegerField()
        start_date = models.DateTimeField()
        end_date = models.DateTimeField()
        list_pdf = models.FileField(upload_to=gen_list_filename, storage=OverwriteFileSystemStorage(), blank=True)

        def __unicode__(self):
                return str(self.year)

        @property
        def status(self):
                if self.start_date and self.end_date:
                        now = timezone.now()
                        if self.start_date < now < self.end_date:
                                return 'in_progress'
                        elif now > self.end_date:
                                return 'finished'
                        else:
                                return 'future'
	        else:
                        return 'N/A'

        def get_scavvies(self):
                self.scavvies.all()

        @models.permalink
        def get_absolute_url(self):
                return ('hunt|show', [self.pk])


class Scavvie(models.Model):
        class Meta:
                unique_together = ('user', 'hunt')

        page_captain = models.BooleanField(default=False)
        captain = models.BooleanField(default=False)
        hunt = models.ForeignKey(Hunt, related_name='scavvies')
        user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')

        def __unicode__(self):
                return self.user.profile.name


class Page(models.Model):
        class Meta:
                unique_together = ('number', 'hunt')

        number = models.IntegerField()
        hunt = models.ForeignKey(Hunt, related_name='pages')
        page_captain = models.ForeignKey(Scavvie, related_name='pages')

        def __unicode__(self):
                return "Page %d" % self.number


class Item(models.Model):
        class Meta:
                unique_together = ('number', 'hunt')

        number = models.IntegerField()
        points = models.DecimalField(max_digits=8, decimal_places=5)
        short_desc = models.CharField(max_length=128)
        full_desc = models.TextField(blank=True)
        completed = models.BooleanField(default=False)
        started = models.BooleanField(default=False)

        page = models.ForeignKey(Page, related_name='items')
        hunt = models.ForeignKey(Hunt, related_name='items')
        page_captain = models.ForeignKey(Scavvie, related_name='captaining_items')
        interested_scavvies = models.ManyToManyField(Scavvie, related_name='interested_items', blank=True)
        working_scavvies = models.ManyToManyField(Scavvie, related_name='working_items', blank=True)
        completed_scavvies = models.ManyToManyField(Scavvie, related_name='completed_items', blank=True)

        def __unicode__(self):
                return "Item %d - %s" % (self.number, self.short_desc)


	@models.permalink
	def get_absolute_url(self):
		return ('item|show', [self.pk])

class Comment(models.Model):
        text = models.CharField(max_length=512)
        item = models.ForeignKey(Item, related_name='comments')
        scavvie = models.ForeignKey(Scavvie, related_name='comments')


class ItemList(models.Model):
        title = models.CharField(max_length=512)
        item = models.ForeignKey(Item, relate_name='')
