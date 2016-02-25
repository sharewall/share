# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-24 12:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('buttons_constructor', '0003_auto_20160224_1238'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=300, verbose_name='page title')),
                ('url', models.URLField(default='', verbose_name='page url')),
                ('page_share_counter', models.IntegerField(default=0, verbose_name='page share counter')),
                ('page_social_traffic', models.IntegerField(default=0, verbose_name='page social network traffic counter')),
            ],
        ),
        migrations.CreateModel(
            name='WebmasterAreaModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_area', models.CharField(default='name area', max_length=200, verbose_name='name area')),
                ('url', models.URLField(default='', verbose_name='url')),
                ('date', models.DateField(auto_now_add=True, verbose_name='date')),
                ('share_today_counter', models.IntegerField(default=0, verbose_name='share today counter')),
                ('share_total_counter', models.IntegerField(default=0, verbose_name='share total counter')),
                ('buttons_constructor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='webmaster_area', to='buttons_constructor.ButtonsConstructorModel', verbose_name='related buttons_constructor')),
            ],
        ),
        migrations.AddField(
            model_name='pagedetail',
            name='webmaster_area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='page_detail', to='webmaster_area.WebmasterAreaModel', verbose_name='related webmaster_area'),
        ),
    ]
