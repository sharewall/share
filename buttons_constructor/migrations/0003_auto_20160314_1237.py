# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-14 12:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buttons_constructor', '0002_buttonsconstructormodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='BtnsImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name image')),
                ('path', models.CharField(max_length=200, verbose_name='path to image')),
                ('type_image', models.CharField(choices=[('CI', 'Circle'), ('SQ', 'Square')], default='CI', max_length=2)),
            ],
        ),
        migrations.RemoveField(
            model_name='buttonsconstructormodel',
            name='cabinet_webmaster',
        ),
        migrations.DeleteModel(
            name='ButtonsConstructorModel',
        ),
    ]
