# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-27 07:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet_webmaster', '0008_auto_20160426_2040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='to_user_pk',
        ),
        migrations.RemoveField(
            model_name='chat',
            name='upload_file',
        ),
    ]
