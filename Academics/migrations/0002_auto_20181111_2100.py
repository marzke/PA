# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-11-11 21:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstructorParent',
            fields=[
                ('emplid', models.CharField(db_column=b'EMPLID', max_length=11, primary_key=True, serialize=False)),
                ('first_name', models.CharField(db_column=b'FIRST_NAME', max_length=30)),
                ('last_name', models.CharField(db_column=b'LAST_NAME', max_length=30)),
                ('emailAddress', models.CharField(db_column=b'EMAIL_ADDR', max_length=30)),
                ('job', models.CharField(db_column=b'JOB', max_length=3)),
                ('desiredLoad', models.IntegerField(db_column=b'DESIRED_LOAD')),
                ('approvedLoad', models.IntegerField(db_column=b'APPROVED_LOAD')),
            ],
            options={
                'db_table': 'INSTRUCTORS_SPRING2018',
                'managed': False,
            },
        ),
        migrations.AddField(
            model_name='section',
            name='acadCareer',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='section',
            name='acadGroup',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='section',
            name='acadOrg',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='section',
            name='associatedClass',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='section',
            name='campus',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='section',
            name='campusEventNumber',
            field=models.CharField(blank=True, max_length=9, null=True),
        ),
        migrations.AddField(
            model_name='section',
            name='classStatus',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='section',
            name='classType',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='section',
            name='combinedSection',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='section',
            name='enrollingStatus',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='section',
            name='institution',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='section',
            name='schedulePrint',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='section',
            name='sessionCode',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
    ]
