# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-08 21:14
from __future__ import unicode_literals

import django.db.models.deletion
import djplaces.fields
from django.db import migrations, models

from app.models import Category

categories = ['one', 'two', 'three', 'four', 'five', 'six', 'seven']


def insert_categories(apps, schema_editor):
    for cat in categories:
        Category.objects.create(name=cat)


class Migration(migrations.Migration):
    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.RunPython(insert_categories),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=1000)),
                ('price_per_day', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='price per day (£)')),
                ('minimum_rental_period', models.IntegerField(verbose_name='minimum rental period (days)')),
                ('estimated_value', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='estimated value (£)')),
                ('place', models.CharField(max_length=250)),
                ('location', djplaces.fields.LocationField()),
                ('categories', models.ManyToManyField(related_name='items', to='app.Category')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Profile')),
                ('renters', models.ManyToManyField(related_name='items', to='app.Profile')),
            ],
        ),
    ]
