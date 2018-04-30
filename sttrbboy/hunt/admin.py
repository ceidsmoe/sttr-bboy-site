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

class PageAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'page_captain')

class ItemAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'number', 'points', 'short_desc', 'completed', 'started', 'hunt', 'page_captain')

class CommentAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'item', 'scavvie')

class TagAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'title')

admin.site.register(Hunt, HuntAdmin)
admin.site.register(Scavvie, ScavvieAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag, TagAdmin)