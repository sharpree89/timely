# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-19 22:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0012_auto_20161119_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appt',
            name='my_location',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='appt',
            name='my_priority',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='appt',
            name='my_status',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='appt',
            name='my_symbol',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='appt',
            name='my_type',
            field=models.CharField(max_length=12),
        ),
    ]
