# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-18 13:37
from __future__ import unicode_literals

import app.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0009_auto_20170112_1024'),
    ]

    operations = [
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('what', models.CharField(blank=True, max_length=250, null=True)),
                ('place', models.CharField(blank=True, max_length=250, null=True)),
                ('location', app.fields.LocationField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
