# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-04-18 02:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academics', '0022_auto_20190418_0148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='positionNumber',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
    ]
