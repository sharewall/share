# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-09 21:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet_webmaster', '0003_cabinetwebmastermodel_money'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cabinetwebmastermodel',
            name='mobile_phone',
            field=models.CharField(default=' ', max_length=200, verbose_name='mobile phone'),
        ),
        migrations.AlterField(
            model_name='cabinetwebmastermodel',
            name='skype',
            field=models.CharField(default=' ', max_length=200, verbose_name='skype'),
        ),
        migrations.AlterField(
            model_name='cabinetwebmastermodel',
            name='wmr',
            field=models.CharField(default=' ', max_length=100, verbose_name='wmr'),
        ),
    ]