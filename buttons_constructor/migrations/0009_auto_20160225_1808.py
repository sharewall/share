# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-25 18:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buttons_constructor', '0008_auto_20160225_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialnetworks',
            name='img_square',
            field=models.URLField(default='', null=True, verbose_name='img_url_square'),
        ),
    ]
