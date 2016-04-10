# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-10 16:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webmaster_area', '0006_auto_20160407_1847'),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaToday',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, verbose_name='date')),
                ('today_social_counter', models.CharField(default='0,0,0,0,0,0,0,0', max_length=300, verbose_name='today social counter(vk,fb,tw,od,gp,ma,li,lj)')),
                ('today_share_counter', models.CharField(default='0,0,0,0,0,0,0,0', max_length=300, verbose_name='today share counter(vk,fb,tw,od,gp,ma,li,lj)')),
            ],
        ),
        migrations.CreateModel(
            name='PageToday',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, verbose_name='date')),
                ('today_social_counter', models.CharField(default='0,0,0,0,0,0,0,0', max_length=300, verbose_name='today social counter(vk,fb,tw,od,gp,ma,li,lj)')),
                ('today_share_counter', models.CharField(default='0,0,0,0,0,0,0,0', max_length=300, verbose_name='today share counter(vk,fb,tw,od,gp,ma,li,lj)')),
            ],
        ),
        migrations.RemoveField(
            model_name='pagedetail',
            name='today_share_counter',
        ),
        migrations.RemoveField(
            model_name='pagedetail',
            name='today_social_counter',
        ),
        migrations.RemoveField(
            model_name='webmasterareamodel',
            name='date',
        ),
        migrations.AddField(
            model_name='webmasterareamodel',
            name='total_share_counter',
            field=models.CharField(default='0,0,0,0,0,0,0,0', max_length=300, verbose_name='total share counter(vk,fb,tw,od,gp,ma,li,lj)'),
        ),
        migrations.AddField(
            model_name='webmasterareamodel',
            name='total_social_counter',
            field=models.CharField(default='0,0,0,0,0,0,0,0', max_length=300, verbose_name='total social counter(vk,fb,tw,od,gp,ma,li,lj)'),
        ),
        migrations.AddField(
            model_name='pagetoday',
            name='page_detail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='page_today', to='webmaster_area.PageDetail', verbose_name='related_page_detail'),
        ),
        migrations.AddField(
            model_name='areatoday',
            name='webmaster_area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='area_today', to='webmaster_area.WebmasterAreaModel', verbose_name='related_webmaster_area'),
        ),
    ]
