# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Youtubeaccountconfig, WeihouaccountConfig, AlipayinfoConfig

# Register your models here.
class YoutubeaccountconfigAdmin(admin.ModelAdmin):
    list_display = ['enabled', 'target_url', 'username', 'password', 'streamersite', 'change_date']
    
admin.site.register(Youtubeaccountconfig, YoutubeaccountconfigAdmin)

class WeihouaccountConfigAdmin(admin.ModelAdmin):
    list_display = ['username', 'password']

admin.site.register(WeihouaccountConfig, WeihouaccountConfigAdmin)

class AlipayinfoConfigAdmin(admin.ModelAdmin):
    list_display = ['appid', 'enabled']
    
admin.site.register(AlipayinfoConfig, AlipayinfoConfigAdmin)
