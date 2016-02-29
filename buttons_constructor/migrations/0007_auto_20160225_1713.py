# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-25 17:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buttons_constructor', '0006_auto_20160225_1706'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='socialnetworks',
            name='img',
        ),
        migrations.AddField(
            model_name='socialnetworks',
            name='img_circle',
            field=models.URLField(default='', null=True, verbose_name='img_url_circle'),
        ),
        migrations.AddField(
            model_name='socialnetworks',
            name='img_square',
            field=models.URLField(default='', null=True, verbose_name='img_url_circle'),
        ),
        migrations.AlterField(
            model_name='buttonsconstructormodel',
            name='social_networks',
            field=models.CharField(default='', max_length=300),
        ),
    ]
