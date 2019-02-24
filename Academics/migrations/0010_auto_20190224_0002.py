# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-02-24 00:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academics', '0009_auto_20190223_1859'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='academicgroup',
            name='admins',
        ),
        migrations.RemoveField(
            model_name='academicgroup',
            name='databaseColumnName',
        ),
        migrations.RemoveField(
            model_name='academicorganization',
            name='admins',
        ),
        migrations.RemoveField(
            model_name='academicorganization',
            name='databaseColumnName',
        ),
        migrations.RemoveField(
            model_name='college',
            name='staff',
        ),
        migrations.RemoveField(
            model_name='department',
            name='faculty',
        ),
        migrations.RemoveField(
            model_name='department',
            name='staff',
        ),
        migrations.AddField(
            model_name='academicorganization',
            name='description',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]
