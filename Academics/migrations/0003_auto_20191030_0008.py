# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-10-30 00:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academics', '0002_course_unitsacadprog'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseattribute',
            name='description',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='courseattribute',
            name='name',
            field=models.CharField(blank=True, max_length=4),
        ),
        migrations.AlterField(
            model_name='courseattribute',
            name='value',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterModelTable(
            name='courseattributeparent',
            table='CLASS_ATTRIBUTE_VW',
        ),
    ]