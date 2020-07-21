# Generated by Django 2.2.13 on 2020-07-21 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_overviews', '0022_courseoverviewtab_is_hidden'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseoverview',
            name='course_image_url',
            field=models.TextField(default='/static/images/default_course_image.jpg'),
        ),
        migrations.AlterField(
            model_name='historicalcourseoverview',
            name='course_image_url',
            field=models.TextField(default='/static/images/default_course_image.jpg'),
        ),
    ]
