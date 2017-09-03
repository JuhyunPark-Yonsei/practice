# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-30 04:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('friend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendship',
            name='from_friend',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='friendship',
            name='to_friend',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_friend_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
