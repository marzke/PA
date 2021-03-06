# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-02-24 03:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Academics', '0010_auto_20190224_0002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawal',
            name='approvedBy',
            field=models.ManyToManyField(blank=True, related_name='approved_withdrawals', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='withdrawal',
            name='deniedBy',
            field=models.ManyToManyField(blank=True, related_name='denied_withdrawals', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='withdrawal',
            name='sectionStudent',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Academics.SectionStudent'),
        ),
    ]
