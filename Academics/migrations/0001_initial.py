# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-11 00:45
from __future__ import unicode_literals

import Academics.fields
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='SectionParent',
            fields=[
                ('id', models.IntegerField(db_column=b'ID', primary_key=True, serialize=False)),
                ('strm', models.CharField(db_column=b'STRM', max_length=4)),
                ('classNumber', models.IntegerField(db_column=b'CLASS_NBR')),
                ('courseID', models.CharField(db_column=b'CRSE_ID', max_length=6)),
                ('subject', models.CharField(db_column=b'SUBJECT', max_length=8)),
                ('catalogNumber', models.CharField(db_column=b'CATALOG_NBR', max_length=10)),
                ('classSection', models.CharField(db_column=b'CLASS_SECTION', max_length=4)),
                ('courseDescription', models.CharField(db_column=b'DESCR', max_length=30)),
                ('units', models.IntegerField(db_column=b'UNITS_ACAD_PROG')),
                ('courseType', models.CharField(db_column=b'SSR_COMPONENT', max_length=3)),
                ('meetDays', models.CharField(db_column=b'MEETING_DAYS', max_length=4)),
                ('startTime', models.CharField(db_column=b'START_TIME', max_length=5)),
                ('endTime', models.CharField(db_column=b'END_TIME', max_length=5)),
                ('startDate', models.CharField(db_column=b'START_DATE', max_length=11)),
                ('endDate', models.CharField(db_column=b'END_DATE', max_length=11)),
                ('building', models.CharField(db_column=b'BLDG_CD', max_length=10)),
                ('room', models.CharField(db_column=b'ROOM', max_length=10)),
                ('enrollCap', models.IntegerField(db_column=b'ENRL_CAP')),
                ('waitCap', models.IntegerField(db_column=b'WAIT_CAP')),
                ('instructorID', models.CharField(db_column=b'EMPLID', max_length=9)),
                ('instructorFirstName', models.CharField(db_column=b'FIRST_NAME', max_length=30)),
                ('instructorLastName', models.CharField(db_column=b'LAST_NAME', max_length=30)),
                ('instructorEmail', models.CharField(db_column=b'EMAIL_ADDR', max_length=40)),
                ('enrollCount', models.IntegerField(db_column=b'ENRL_TOT')),
                ('waitCount', models.IntegerField(db_column=b'WAIT_TOT')),
                ('enrollingStatus', models.CharField(db_column=b'ENRL_STAT', max_length=1)),
                ('classStatus', models.CharField(db_column=b'CLASS_STAT', max_length=1)),
                ('classType', models.CharField(db_column=b'CLASS_TYPE', max_length=1)),
                ('associatedClass', models.IntegerField(db_column=b'ASSOCIATED_CLASS')),
                ('schedulePrint', models.CharField(db_column=b'SCHEDULE_PRINT', max_length=1)),
                ('acadOrg', models.CharField(db_column=b'ACAD_ORG', max_length=10)),
                ('acadCareer', models.CharField(db_column=b'ACAD_CAREER', max_length=4)),
                ('acadGroup', models.CharField(db_column=b'ACAD_GROUP', max_length=5)),
                ('institution', models.CharField(db_column=b'INSTITUTION', max_length=5)),
                ('campus', models.CharField(db_column=b'CAMPUS', max_length=5)),
                ('campusEventNumber', models.CharField(db_column=b'CAMPUS_EVENT_NBR', max_length=9)),
                ('combinedSection', models.CharField(db_column=b'COMBINED_SECTION', max_length=1)),
                ('sessionCode', models.CharField(db_column=b'SESSION_CODE', max_length=3)),
            ],
            options={
                'db_table': 'SECTION_VW',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SectionStudentParent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(db_column=b'STRM', max_length=4)),
                ('classNumber', models.IntegerField(db_column=b'CLASS_NBR')),
                ('subject', models.CharField(db_column=b'SUBJECT', max_length=8)),
                ('catalogNumber', models.CharField(db_column=b'CATALOG_NBR', max_length=10)),
                ('classSection', models.CharField(db_column=b'CLASS_SECTION', max_length=4)),
                ('username', models.CharField(db_column=b'EMPLID', max_length=11)),
                ('first_name', models.CharField(db_column=b'FIRST_NAME', max_length=30)),
                ('last_name', models.CharField(db_column=b'LAST_NAME', max_length=30)),
                ('email', models.CharField(db_column=b'EMAIL_ADDR', max_length=40)),
                ('status', models.CharField(db_column=b'ENROLLED_STATUS', max_length=8)),
            ],
            options={
                'db_table': 'PA_ENROLL_SPRING2017_VW',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AcademicGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('databaseColumnName', models.CharField(max_length=5)),
                ('description', models.CharField(blank=True, max_length=60, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AcademicOrganization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('databaseColumnName', models.CharField(max_length=10)),
                ('description', models.CharField(blank=True, max_length=60, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.SmallIntegerField(choices=[(b'Semester', b'Semester'), (b'OneYear', b'OneYear'), (b'ThreeYear', b'ThreeYear')])),
                ('timeBase', models.DecimalField(decimal_places=2, max_digits=8)),
                ('monthlyBaseSalary', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=8)),
                ('title', models.CharField(blank=True, max_length=128, null=True)),
                ('units', models.SmallIntegerField(blank=True, null=True)),
                ('academicGroup', models.SmallIntegerField(blank=True, null=True)),
                ('semestersOffered', models.CharField(blank=True, choices=[(b'', b'Unknown'), (b'FallSpring', b'Fall and Spring'), (b'Fall', b'Fall'), (b'Spring', b'Spring')], max_length=16)),
                ('yearsOffered', models.CharField(blank=True, choices=[(b'', b'Unknown'), (b'EvenOdd', b'Even and Odd'), (b'Even', b'Even'), (b'Odd', b'Odd')], max_length=16)),
                ('corequisites', models.ManyToManyField(blank=True, related_name='corequisites_to', to='Academics.Course')),
            ],
        ),
        migrations.CreateModel(
            name='CourseType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[(b'LEC', b'Lecture'), (b'LAB', b'Lab'), (b'SEM', b'Seminar'), (b'SUP', b'Supervision'), (b'ACT', b'Activity'), (b'FLD', b'Field Studies')], max_length=8)),
                ('description', models.CharField(blank=True, max_length=60, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='KFactor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minCSNumber', models.SmallIntegerField(blank=True, null=True)),
                ('maxCSNumber', models.SmallIntegerField(blank=True, null=True)),
                ('factor', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departmentCode', models.CharField(max_length=4)),
                ('positionCode', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Prerequisite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passingGrade', Academics.fields.GradeField(blank=True, choices=[(Academics.fields.Grade(b'A'), Academics.fields.Grade(b'A')), (Academics.fields.Grade(b'A-'), Academics.fields.Grade(b'A-')), (Academics.fields.Grade(b'B+'), Academics.fields.Grade(b'B+')), (Academics.fields.Grade(b'B'), Academics.fields.Grade(b'B')), (Academics.fields.Grade(b'B-'), Academics.fields.Grade(b'B-')), (Academics.fields.Grade(b'C+'), Academics.fields.Grade(b'C+')), (Academics.fields.Grade(b'C'), Academics.fields.Grade(b'C')), (Academics.fields.Grade(b'C-'), Academics.fields.Grade(b'C-')), (Academics.fields.Grade(b'D+'), Academics.fields.Grade(b'D+')), (Academics.fields.Grade(b'D'), Academics.fields.Grade(b'D')), (Academics.fields.Grade(b'D-'), Academics.fields.Grade(b'D-')), (Academics.fields.Grade(b'WU'), Academics.fields.Grade(b'WU')), (Academics.fields.Grade(b'F'), Academics.fields.Grade(b'F')), (Academics.fields.Grade(b'IC'), Academics.fields.Grade(b'IC')), (Academics.fields.Grade(b''), Academics.fields.Grade(b'')), (Academics.fields.Grade(b'WM'), Academics.fields.Grade(b'WM')), (Academics.fields.Grade(b'AUD'), Academics.fields.Grade(b'AUD')), (Academics.fields.Grade(b'RP'), Academics.fields.Grade(b'RP')), (Academics.fields.Grade(b'NC'), Academics.fields.Grade(b'NC')), (Academics.fields.Grade(b'RD'), Academics.fields.Grade(b'RD')), (Academics.fields.Grade(b'I'), Academics.fields.Grade(b'I')), (Academics.fields.Grade(b'IP'), Academics.fields.Grade(b'IP')), (Academics.fields.Grade(b'AU'), Academics.fields.Grade(b'AU')), (Academics.fields.Grade(b'W'), Academics.fields.Grade(b'W')), (Academics.fields.Grade(b'CR'), Academics.fields.Grade(b'CR')), (Academics.fields.Grade(b'Conc'), Academics.fields.Grade(b'Conc'))], max_length=4)),
                ('requiredCourse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prerequisiteCourses', to='Academics.Course')),
                ('requiredForCourse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coursesWithPrerequisites', to='Academics.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=4)),
                ('classNumber', models.IntegerField()),
                ('meetDays', models.CharField(blank=True, max_length=32, null=True)),
                ('startTime', models.TimeField(blank=True, null=True)),
                ('endTime', models.TimeField(blank=True, null=True)),
                ('room', models.CharField(blank=True, max_length=32, null=True)),
                ('roomCap', models.IntegerField(blank=True, null=True)),
                ('enrollCap', models.IntegerField(blank=True, null=True)),
                ('waitCap', models.IntegerField(blank=True, null=True)),
                ('conflicts', models.ManyToManyField(blank=True, related_name='_section_conflicts_+', to='Academics.Section')),
                ('courseType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Academics.CourseType')),
                ('kFactor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Academics.KFactor')),
            ],
        ),
        migrations.CreateModel(
            name='SectionPreference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preference', models.IntegerField(blank=True, null=True)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Academics.Section')),
            ],
        ),
        migrations.CreateModel(
            name='SectionStudent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[(b'ENROLLED', b'Enrolled'), (b'WAITLISTED', b'Waitlisted'), (b'UNREGISTERED', b'Unregistered'), (b'DROPPED', b'Dropped')], max_length=32)),
                ('permissionNumber', models.BigIntegerField(blank=True, null=True)),
                ('entryDate', models.DateField(auto_now_add=True)),
                ('updateDate', models.DateField(auto_now=True)),
                ('passedPrerequisites', models.NullBooleanField(default=None)),
                ('passedExams', models.NullBooleanField(default=None)),
                ('qualified', models.NullBooleanField(default=None)),
                ('grade', Academics.fields.GradeField(blank=True, max_length=4)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Academics.Section')),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='StudentGrade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', Academics.fields.GradeField(blank=True, max_length=4)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Academics.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=8, unique=True)),
                ('description', models.CharField(blank=True, max_length=60, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season', models.CharField(choices=[(b'1', b'Winter'), (b'3', b'Spring'), (b'5', b'Summer'), (b'7', b'Fall')], max_length=20)),
                ('year', models.CharField(max_length=4)),
                ('number', models.CharField(max_length=4, unique=True)),
                ('startDate', models.DateField(blank=True, null=True)),
                ('endDate', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TermInstructor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requestedLoad', models.IntegerField(blank=True, null=True)),
                ('approvedLoad', models.IntegerField(blank=True, null=True)),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Academics.Term')),
            ],
        ),
        migrations.CreateModel(
            name='WeeklyEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=1)),
                ('startTime', models.TimeField()),
                ('endTime', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.ASCIIUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'person',
                'verbose_name_plural': 'people',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('academicgroup_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Academics.AcademicGroup')),
            ],
            bases=('Academics.academicgroup',),
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('academicorganization_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Academics.AcademicOrganization')),
            ],
            bases=('Academics.academicorganization',),
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('gta', models.NullBooleanField()),
                ('priority', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'instructor',
                'verbose_name_plural': 'instructors',
            },
            bases=('Academics.person',),
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('academicorganization_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Academics.AcademicOrganization')),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Academics.College')),
            ],
            bases=('Academics.academicorganization',),
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('academicorganization_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Academics.AcademicOrganization')),
            ],
            bases=('Academics.academicorganization',),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('level', models.CharField(choices=[(b'Freshman', b'Freshman'), (b'Sophomore', b'Sophomore'), (b'Junior', b'Junior'), (b'Senior', b'Senior'), (b'Post-Bacc', b'Post-Bacc'), (b'Graduate', b'Graduate')], max_length=16)),
            ],
            options={
                'verbose_name': 'student',
                'verbose_name_plural': 'students',
            },
            bases=('Academics.person',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='person',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='weeklyevent',
            unique_together=set([('day', 'startTime', 'endTime')]),
        ),
        migrations.AddField(
            model_name='subject',
            name='host',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Academics.AcademicOrganization'),
        ),
        migrations.AddField(
            model_name='session',
            name='coordinator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='session',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Academics.Course'),
        ),
        migrations.AddField(
            model_name='session',
            name='term',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Academics.Term'),
        ),
        migrations.AddField(
            model_name='section',
            name='meetings',
            field=models.ManyToManyField(blank=True, to='Academics.WeeklyEvent'),
        ),
        migrations.AddField(
            model_name='section',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Academics.Session'),
        ),
        migrations.AddField(
            model_name='position',
            name='employees',
            field=models.ManyToManyField(through='Academics.Appointment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='prerequisites',
            field=models.ManyToManyField(blank=True, related_name='prerequisites_to', through='Academics.Prerequisite', to='Academics.Course'),
        ),
        migrations.AddField(
            model_name='course',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Academics.Subject'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointment',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Academics.Position'),
        ),
        migrations.AddField(
            model_name='academicorganization',
            name='admins',
            field=models.ManyToManyField(blank=True, null=True, related_name='academic_orgs_as_admin', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='academicgroup',
            name='admins',
            field=models.ManyToManyField(blank=True, null=True, related_name='academic_groups_as_admin', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='terminstructor',
            name='instructor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Academics.Instructor'),
        ),
        migrations.AddField(
            model_name='term',
            name='instructors',
            field=models.ManyToManyField(blank=True, through='Academics.TermInstructor', to='Academics.Instructor'),
        ),
        migrations.AddField(
            model_name='studentgrade',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Academics.Student'),
        ),
        migrations.AlterUniqueTogether(
            name='session',
            unique_together=set([('course', 'term')]),
        ),
        migrations.AddField(
            model_name='sectionstudent',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Academics.Student'),
        ),
        migrations.AddField(
            model_name='sectionpreference',
            name='instructor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Academics.Instructor'),
        ),
        migrations.AddField(
            model_name='section',
            name='instructor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Academics.Instructor'),
        ),
        migrations.AddField(
            model_name='section',
            name='students',
            field=models.ManyToManyField(blank=True, through='Academics.SectionStudent', to='Academics.Student'),
        ),
        migrations.AddField(
            model_name='school',
            name='aoc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='schools_is_aoc', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='school',
            name='college',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Academics.College'),
        ),
        migrations.AddField(
            model_name='school',
            name='director',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='schools_is_director', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='program',
            name='director',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='programs_is_director', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='instructor',
            name='preferences',
            field=models.ManyToManyField(blank=True, related_name='requested_by', through='Academics.SectionPreference', to='Academics.Section'),
        ),
        migrations.AddField(
            model_name='department',
            name='aoc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='departments_is_aoc', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='department',
            name='chair',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='departments_is_chair', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='department',
            name='college',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Academics.College'),
        ),
        migrations.AddField(
            model_name='department',
            name='faculty',
            field=models.ManyToManyField(blank=True, null=True, related_name='departments_is_faculty', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='department',
            name='staff',
            field=models.ManyToManyField(blank=True, null=True, related_name='departments_is_staff', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='studentGrades',
            field=models.ManyToManyField(blank=True, related_name='courseGrades', through='Academics.StudentGrade', to='Academics.Student'),
        ),
        migrations.AddField(
            model_name='college',
            name='dean',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='colleges_is_dean', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='college',
            name='staff',
            field=models.ManyToManyField(blank=True, null=True, related_name='colleges_is_staff', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='sectionpreference',
            unique_together=set([('section', 'instructor')]),
        ),
        migrations.AlterUniqueTogether(
            name='section',
            unique_together=set([('session', 'number')]),
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together=set([('subject', 'number')]),
        ),
    ]