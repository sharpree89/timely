# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-19 20:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_auto_20161119_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appt',
            name='my_symbol',
            field=models.CharField(max_length=12),
        ),
    ]
