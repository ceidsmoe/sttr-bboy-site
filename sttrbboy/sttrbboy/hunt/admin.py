# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from sttrbboy.hunt.models import *

# Register your models here.
class HuntAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'year', 'start_date', 'end_date')
	readonly_fields = ['status']

class ScavvieAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'user', 'hunt', 'page_captain', 'captain')


admin.site.register(Hunt, HuntAdmin)
admin.site.register(Scavvie, ScavvieAdmin)