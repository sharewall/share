# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-25 17:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buttons_constructor', '0007_auto_20160225_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buttonsconstructormodel',
            name='social_networks',
            field=models.CharField(default='vk,fb,tw,od,gp,ma,li,lj', max_length=300),
        ),
    ]
