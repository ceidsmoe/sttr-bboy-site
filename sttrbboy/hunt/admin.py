# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.db.models import Q
from sttrbboy.hunt.models import *

# Register your models here.
class HuntAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'year', 'start_date', 'end_date')
	readonly_fields = ['status']

class ScavvieAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'user', 'hunt', 'page_captain', 'captain')
	list_filter = ('hunt', 'page_captain', 'captain')

class PageAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'page_captain')
	list_filter = ('olympics', 'roadtrip', 'hunt')

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.remote_field.model == Scavvie and not request.user.is_superuser:
			kwargs['queryset'] = Scavvie.objects.filter(Q(hunt=Hunt.objects.all()[Hunt.objects.count()-1]), Q(page_captain=True) | Q(captain=True))

		return super(PageAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class ItemAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'number', 'points', 'short_desc', 'completed', 'started', 'hunt')
	list_filter = ('olympics', 'roadtrip', 'hunt')

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		kwargs['queryset'] = Page.objects.filter(hunt=Hunt.objects.all()[Hunt.objects.count()-1])
		return super(ItemAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

	def get_form(self, request, obj=None, **kwargs):
		self.exclude = ("page_captain", "hunt",)
		return super(ItemAdmin, self).get_form(request, obj, **kwargs)

	def save_model(self, request, obj, form, change):
		obj.page_captain = obj.page.page_captain
		obj.hunt = obj.page.hunt
		super(ItemAdmin, self).save_model(request, obj, form, change)

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