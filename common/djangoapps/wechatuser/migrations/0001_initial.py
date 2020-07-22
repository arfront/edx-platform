# Generated by Django 2.2.13 on 2020-07-22 03:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WechatUserconfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change_date', models.DateTimeField(auto_now_add=True, verbose_name='Change date')),
                ('enabled', models.BooleanField(default=False, verbose_name='Enabled')),
                ('key', models.TextField(blank=True, verbose_name='Client ID')),
                ('secret', models.TextField(blank=True, verbose_name='Client Secret')),
                ('changed_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Changed by')),
            ],
            options={
                'db_table': 'wechat_user_h5_config',
                'verbose_name': 'Wechat Config(h5 page)',
                'verbose_name_plural': 'Wechat Config(h5 page)',
            },
        ),
    ]
