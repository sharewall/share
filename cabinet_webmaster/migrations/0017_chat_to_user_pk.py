# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-10 16:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet_webmaster', '0016_auto_20160510_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='to_user_pk',
            field=models.IntegerField(blank=True, null=True, verbose_name='to_user_pk'),
        ),
    ]