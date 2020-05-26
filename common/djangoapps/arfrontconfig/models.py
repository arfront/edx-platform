# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import uuid
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


class AlipayinfoConfig(ConfigurationModel):
    
    appid = models.TextField(blank=True, verbose_name='appid')
    app_private_key = models.TextField(blank=True, verbose_name='app_private_key')
    alipay_public_key = models.TextField(blank=True, verbose_name='alipay_public_key')
    
    class Meta:
        db_table = "alipayinfoconfig"
        app_label = "arfrontconfig"
        verbose_name = "Alipay info"
        verbose_name_plural = verbose_name



def user_directory_path(instance, filename):
    ext = filename.split('.').pop()
    filename = '{0}.{1}'.format(uuid.uuid4(), ext)
    return os.path.join(filename)


class Lmsbannerlist(models.Model):
    
    id = models.AutoField(primary_key=True)
    banner = models.ImageField(verbose_name='banner path', upload_to=user_directory_path, default='')
    order_id = models.IntegerField(default=1, verbose_name='Sort')
    
    class Meta:
        db_table = "lmsbannerlist"
        app_label = "arfrontconfig"
        verbose_name = "Lms banner"
        verbose_name_plural = verbose_name
        
    def banner_url(self):
        if self.banner and hasattr(self.banner, 'url'):
            return self.banner.url
        else:
            return '/static/images/lms_banner.jpg'

CONTENT_TYPES = (
    ('honor', 'honor'),
    ('tos', 'tos'),
    ('privacy', 'privacy')
)

class AricleContent(models.Model):
    
    id = models.AutoField(primary_key=True)
    content_type = models.CharField(choices=CONTENT_TYPES, unique=True, max_length=32, default='privacy')
    content = models.TextField()
    
    class Meta:
        db_table = "aritlecontent"
        app_label = "arfrontconfig"
        verbose_name = "aricle content"
        verbose_name_plural = verbose_name


class RecordVerifyCodeDetail(models.Model):
    
    id = models.AutoField(primary_key=True)
    phonenum = models.CharField(max_length=128, default='', blank=True)
    code = models.CharField(max_length=128, default='', blank=True)
    is_active = models.IntegerField(default=1, verbose_name='验证吗是否有效')  # 0 无效 1　有效
    send_type = models.CharField(default='', max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'recordverifycodedetail'
        app_label = "arfrontconfig"
        verbose_name = "record verify code detail"
        verbose_name_plural = verbose_name
    
    
class SmsDetailConfig(ConfigurationModel):
    
    account = models.CharField(max_length=128, default='', verbose_name='Account')
    pwd = models.CharField(max_length=128, default='', verbose_name='Pwd')
    content = models.CharField(max_length=256, default='', verbose_name='Content')
    templateid = models.CharField(max_length=128, default='', verbose_name='TemplateId')
    signid = models.CharField(max_length=128, default='', verbose_name='SignId')
    
    class Meta:
        db_table = "smsdetailconfig"
        app_label = "arfrontconfig"
        verbose_name = "Sms detail"
        verbose_name_plural = verbose_name
