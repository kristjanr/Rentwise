# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-22 16:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20170119_1957'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='email_sent_to_user',
            field=models.BooleanField(default=False),
        ),
    ]