# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from sttrbboy.users.models import *

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
	search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone_number')

admin.site.register(Profile, ProfileAdmin)