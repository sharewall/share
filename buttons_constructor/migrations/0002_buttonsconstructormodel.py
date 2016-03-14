# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-14 12:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet_webmaster', '0006_auto_20160309_2147'),
        ('buttons_constructor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ButtonsConstructorModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_constructor', models.CharField(default='name constructor', max_length=50, verbose_name='name_constructor')),
                ('social_networks', models.CharField(default='', max_length=300)),
                ('with_counter', models.BooleanField(default=True)),
                ('form_buttons', models.CharField(choices=[('CI', 'Circle'), ('SQ', 'Square')], default='CI', max_length=2)),
                ('location_buttons', models.CharField(choices=[('HO', 'Horizontal'), ('VE', 'Vertical')], default='HO', max_length=2)),
                ('size_buttons', models.CharField(choices=[('BIG', 'Big'), ('MED', 'Medium'), ('SML', 'Small')], default='MED', max_length=3)),
                ('mobile_view', models.BooleanField(default=False)),
                ('with_background', models.BooleanField(default=False)),
                ('background_color', models.TextField(default='rgb(255, 255, 255)')),
                ('page_url', models.URLField(blank=True, default='')),
                ('page_title', models.CharField(blank=True, default='', max_length=200)),
                ('page_description', models.TextField(blank=True, default='')),
                ('cabinet_webmaster', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buttons_constructor', to='cabinet_webmaster.CabinetWebmasterModel', verbose_name='related cabinet webmaster')),
            ],
        ),
    ]