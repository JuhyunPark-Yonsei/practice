# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-27 04:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prac', '0002_auto_20170827_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='user_agent',
            field=models.CharField(default='default', max_length=200),
            preserve_default=False,
        ),
    ]
