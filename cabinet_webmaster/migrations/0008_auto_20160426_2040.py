# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-26 20:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet_webmaster', '0007_chat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='to_user_pk',
            field=models.IntegerField(blank=True, null=True, verbose_name='to_user_pk'),
        ),
    ]