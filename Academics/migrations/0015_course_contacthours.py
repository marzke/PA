# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-04-03 23:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academics', '0014_course_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='contactHours',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]