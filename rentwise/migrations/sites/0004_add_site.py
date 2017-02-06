# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def insert_sites(apps, schema_editor):
    """Populate the sites model"""
    Site = apps.get_model('sites', 'Site')
    Site.objects.all().delete()

    Site.objects.create(id=2, domain='rentwise.herokuapp.com', name='YBuy')


class Migration(migrations.Migration):
    dependencies = [
        ('sites', '0003_auto_20170109_1752'),
    ]

    operations = [
        migrations.RunPython(insert_sites)
    ]
