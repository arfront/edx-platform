# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import DingtalkUserconfig


# Register your models here.

class DingtalkUserconfigAdmin(admin.ModelAdmin):
    list_display = ['enabled', 'key', 'secret', 'change_date']

admin.site.register(DingtalkUserconfig, DingtalkUserconfigAdmin)
