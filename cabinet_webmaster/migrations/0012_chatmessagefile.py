# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-27 09:01
from __future__ import unicode_literals

import cabinet_webmaster.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet_webmaster', '0011_auto_20160427_0838'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatMessageFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_store', models.FileField(upload_to=cabinet_webmaster.models.generate_filename)),
                ('chat_message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_message_file', to='cabinet_webmaster.ChatMessage', verbose_name='related_chat_message')),
            ],
        ),
    ]
