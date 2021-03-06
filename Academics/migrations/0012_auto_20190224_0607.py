# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-02-24 06:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Academics', '0011_auto_20190224_0322'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reason',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('description', models.CharField(blank=True, max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='WithdrawalReason',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.SmallIntegerField()),
                ('reason', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Academics.Reason')),
                ('withdrawalPreferences', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Academics.WithdrawalPreferences')),
            ],
        ),
        migrations.AddField(
            model_name='withdrawalpreferences',
            name='reasons',
            field=models.ManyToManyField(through='Academics.WithdrawalReason', to='Academics.Reason'),
        ),
    ]
