from django.contrib import admin

# Register your models here.
from .models import DingtalkUserconfig


# Register your models here.

class DingtalkUserconfigAdmin(admin.ModelAdmin):
    list_display = ['enabled', 'key', 'secret', 'change_date']

admin.site.register(DingtalkUserconfig, DingtalkUserconfigAdmin)