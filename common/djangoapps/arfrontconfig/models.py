# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from config_models.models import ConfigurationModel


# Create your models here.
class Youtubeaccountconfig(ConfigurationModel):
    
    username = models.TextField(blank=True, verbose_name="User")
    password = models.TextField(blank=True, verbose_name="Password")
    streamersite = models.TextField(blank=True, verbose_name="Streamer Site")
    target_url = models.TextField(blank=True, verbose_name="Target url")
    
    class Meta:
        db_table = "youtubeaccountconfig"
        app_label = "arfrontconfig"
        verbose_name = "Youtube account(h5 page)"
        verbose_name_plural = verbose_name


class WeihouaccountConfig(ConfigurationModel):
    
    username = models.TextField(blank=True, verbose_name='User')
    password = models.TextField(blank=True, verbose_name='Password')
    
    class Meta:
        db_table = "weihouaccountconfig"
        app_label = "arfrontconfig"
        verbose_name = "Weihou account"
        verbose_name_plural = verbose_name
        

class NewerguideRecord(models.Model):
    
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(blank=False)
    live_guide = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'newerguiderecord'
        app_label = "arfrontconfig"
