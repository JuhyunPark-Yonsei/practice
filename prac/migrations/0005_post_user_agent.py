# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-30 04:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prac', '0004_remove_post_user_agent'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='user_agent',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
