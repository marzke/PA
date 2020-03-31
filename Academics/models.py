import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, Group
from .fields import *
from django.db import connections
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
import re
import datetime
import pandas as pd
import sys

#from Academics.fields import *
import numpy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WeeklyEvent(models.Model):

    day = models.CharField(max_length=1)
    startTime = models.TimeField()
    endTime = models.TimeField()

    class Meta:
        unique_together = (('day', 'startTime','endTime'),)

    def start(self):
        masterMonday = datetime.date(2016, 8, 15)
        dayOfWeek = ['M','T','W','R','F'].index(self.day)
        date = masterMonday + datetime.timedelta(days=dayOfWeek)
        return datetime.datetime.combine(date, self.startTime)

    def finish(self):
        masterMonday = datetime.date(2016, 8, 15)
        dayOfWeek = ['M', 'T', 'W', 'R', 'F'].index(self.day)
        date = masterMonday + datetime.timedelta(days=dayOfWeek)
        return datetime.datetime.combine(date, self.endTime)

    def conflictsWith(self, other):
#        if not isinstance(other, WeeklyEvent):
#            raise
        return ((self.start() <= other.start() < self.finish()) or
                (self.start() < other.finish() <= self.finish()) or
                (other.start() <= self.start() < other.finish()) or
                (other.start() < self.finish() <= other.finish()))

    def __unicode__(self):
        return '{0}  {1} - {2}'.format(self.day, self.startTime, self.endTime)


class PersonManager(UserManager):

    def checkSelfConflicts(self, termNumber=''):
        for person in self.all():
            conflict = person.checkSelfConflicts(termNumber=termNumber)
            if conflict:
                print person, 'has self conflicts'


class Person(AbstractUser):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    preferences = models.ManyToManyField(
        'Section', blank=True,
        through='SectionPreference', related_name='requested_by'
    )
    objects = PersonManager()

    class Meta:
        verbose_name = 'person'
        verbose_name_plural = 'people'

#    def save(self, *args, **kwargs):
#            self.set_unusable_password()
#            super(Person, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'{0}  {2} {1}'.format(self.username, self.last_name,
                                      self.first_name)

# roles are handled as permissions using auth 2017-01-16
# note instructor is a role, not a type of Person
# types of Person are determined by job classification
# (or enrollment status in the case of a student)

    def conflictsWith(self, section=None):
        if not section:
            return False
        try:
            sectionsAsStudent = list(self.student.section_set.filter(
                session__term__number=section.session.term.number
            ))
        except:
            sectionsAsStudent = []
        try:
            sectionsAsInstructor = list(self.sectionsAsInstructor.filter(
                session__term__number=section.session.term.number
            ))
        except:
            sectionsAsInstructor = []
        #print sectionsAsStudent
        #print sectionsAsInstructor
        commitments = sectionsAsStudent + sectionsAsInstructor
        #print commitments
        for commitment in commitments:
            #print 'testing ', commitment, section
            conflict = commitment.conflictsWith(section)
            if conflict:
                #print 'CONFLICT'
                return True
        return False


    # need to try section_set (for students) AND sectionsAsInstructor (for students and lecturers)

    def checkSelfConflicts(self, termNumber=''):

        try:
            sectionsAsStudent = list(self.student_ptr.section_set.filter(
                session__term__number=termNumber
            ))
        except:
            sectionsAsStudent = []
        try:
            sectionsAsInstructor = list(self.sectionsAsInstructor.filter(
                session__term__number=termNumber
            ))
        except:
            sectionsAsInstructor = []
        sections = sectionsAsStudent + sectionsAsInstructor
        #print self.__unicode__(), sections
        n = len(sections)
        for i in range(n):
            for j in range(i+1, n):
                conflict = sections[i].conflictsWith(sections[j])
                if conflict:
                    print i, j, self.first_name, self.last_name, sections[i], sections[j]
                    return True
        return False





#class Instructor(Person):

    #gta = models.NullBooleanField(blank=True, null=True)
    #priority = models.IntegerField(blank=True, null=True)


class StudentManager(PersonManager):

    def get_or_create_with_person(self, **kwargs):
        newStudent = False
        oldPerson = False
        try:
            student = self.get(username=kwargs['username'])
        except:
            newStudent = True
            try:
                student = self.create(**kwargs)
                student.save()
            except:
                oldPerson = True
                person = Person.objects.get(username=kwargs['username'])
                student = self.create(person_ptr=person, level=kwargs['level'])
                student.__dict__.update(person.__dict__)
                student.save()
        return (student, newStudent, oldPerson,)


class Student(Person):

    class Meta:
        verbose_name = 'student'
        verbose_name_plural = 'students'

    #degreeProgram = models.ManyToManyField('DegreeProgram')
    objects = StudentManager()
    level = models.CharField(max_length=16, choices=(
        ('Freshman', 'Freshman'),
        ('Sophomore','Sophomore'),
        ('Junior', 'Junior'),
        ('Senior', 'Senior'),
        ('Post-Bacc', 'Post-Bacc'),
        ('Graduate', 'Graduate'),
    ))


class EmployeeParent(models.Model):

    emplid = models.CharField(max_length=11, db_column='EMPLID', primary_key=True)
    firstName = models.CharField(max_length=30, db_column='FIRST_NAME')
    lastName = models.CharField(max_length=30, db_column='LAST_NAME')
    emailAddress = models.CharField(max_length=30, db_column='EMAIL_ADDR')
    jobCode = models.CharField(max_length=128, db_column='JOB_CODE')
    jobDescription = models.CharField(max_length=128, db_column='JOB_DESCRIPTION')
    jobAbbreviation = models.CharField(max_length=128, db_column='JOB_ABBR')
    jobFunction = models.CharField(max_length=128, db_column='JOB_FUNCTION')
    jobTitle = models.CharField(max_length=128, db_column='JOB_TITLE')
    jobGrade = models.CharField(max_length=128, db_column='JOB_GRADE')

    class Meta:
        managed = False
        db_table = 'EMPLOYEE'

    def __unicode__(self):
        return '{0}  {1}  {2} {3}'.format(
            self.emplid, self.firstName, self.lastName, self.jobDescription,
        )


class PositionManager(models.Manager):

    def importFromExcel(self, file):
        df = pd.read_excel(file, header=1, na_values=['NA'])
        for i in range(len(df['UIN'])):
            person, new = Person.objects.get_or_create(username=df['UIN'].iloc[i])
            if new:
                person.last_name = df['Last'].iloc[i]
                person.first_name = df['First Name'].iloc[i]
            deptID = df['Dept ID'].iloc[i]
            dept = df['Department'].iloc[i]
            jobCode = df['Job Code'].iloc[i]
            grade = df['Grade'].iloc[i]
            FTCompRate = df['FT Comp Rate'].iloc[i]
            timeBase = df['Time Base'].iloc[i]
            monthlySalary = df['Monthly Salary'].iloc[i]
            positionNumber = df['Position #'].iloc[i]
            firstHireDate = df['First Hire Date'].iloc[i]
            effectiveDate = df['Eff Date'].iloc[i]
            apptEndDate = df['Appt End Date'].iloc[i]
            payStatus = df['Pay Status'].iloc[i]
            actionDate = df['Action Date'].iloc[i]
            position, new = self.get_or_create(
                person=person, departmentID=deptID, department=dept,
                jobCode=jobCode, grade=grade, fullTimeCompRate=FTCompRate,
                timeBase=timeBase, monthlySalary=monthlySalary,
                positionNumber=positionNumber, firstHireDate=firstHireDate,
                effectiveDate=effectiveDate,
                actionDate=actionDate,
            )
            #print position, payStatus, position.payStatus
            #print payStatus == numpy.nan
            if type(apptEndDate) == datetime.date:
                position.apptEndDate = apptEndDate
            if type(payStatus) == unicode:
                position.payStatus = payStatus
            #return position
            position.save()


# based on HRMS query SFO_FACULTY_ROSTER_ACTION_DT
class Position(models.Model):

    jobCode = models.SmallIntegerField()
    department = models.CharField(max_length=64)
    departmentID = models.SmallIntegerField()
    person = models.ForeignKey(Person, blank=True, null=True)
    grade = models.SmallIntegerField(blank=True, null=True)
    fullTimeCompRate = models.FloatField(blank=True, null=True)
    timeBase = models.FloatField()
    monthlySalary = models.FloatField(blank=True, null=True)
    positionNumber = models.CharField(max_length=8, blank=True, null=True)
    firstHireDate = models.DateField(blank=True, null=True)
    effectiveDate = models.DateField(blank=True, null=True)
    apptEndDate = models.DateField(blank=True, null=True)
    payStatus = models.CharField(max_length=16, blank=True, null=True)
    actionDate = models.DateField(blank=True, null=True)

    objects = PositionManager()

    def __unicode__(self):
        return "{0}   {1} ({2})".format(self.person, self.jobCode, self.department)



class InstructorParent(models.Model):

    emplid = models.CharField(max_length=11, db_column='EMPLID', primary_key=True)
    first_name = models.CharField(max_length=30, db_column='FIRST_NAME')
    last_name = models.CharField(max_length=30, db_column='LAST_NAME')
    emailAddress = models.CharField(max_length=30, db_column='EMAIL_ADDR')
    job = models.CharField(max_length=3, db_column='JOB')
    desiredLoad = models.IntegerField(db_column='DESIRED_LOAD')
    approvedLoad = models.IntegerField(db_column='APPROVED_LOAD')

    class Meta:
        managed = False
        db_table = 'INSTRUCTORS_SPRING2018'

    def __unicode__(self):
        return '{0}  {1}  {2} {3}'.format(
            self.emplid, self.first_name, self.last_name, self.job,
        )

class LecturerManager(PersonManager):

    def get_or_create_with_person(self, **kwargs):
        newLecturer = False
        oldPerson = False
        try:
            lecturer = self.get(username=kwargs['username'])
        except:
            newLecturer = True
            try:
                lecturer = self.create(**kwargs)
                lecturer.save()
            except:
                oldPerson = True
                person = Person.objects.get(username=kwargs['username'])
                lecturer = self.create(person_ptr=person)
                lecturer.__dict__.update(person.__dict__)
                lecturer.save()
        return (lecturer, newLecturer, oldPerson,)

    def create_from_parent_employees(self):
        pLecturers = EmployeeParent.objects.filter(jobFunction__contains='LEC')
        for pLecturer in pLecturers:
            newLecturer = False
            oldPerson = False
            try:
                lecturer = self.get(username=pLecturer.emplid)
            except:
                newLecturer = True
                try:
                    lecturer = self.create(**kwargs)
                    lecturer.save()
                except:
                    oldPerson = True
                    person = Person.objects.get(username=pLecturer.emplid)
                    lecturer = self.create(person_ptr=person)
                    lecturer.__dict__.update(person.__dict__)
                    lecturer.save()

    def update_from_instructor_table(self):
        parents = InstructorParent.objects.filter(job='LEC')
        for parent in parents:
            lec, newLEC, oldPerson = self.get_or_create_with_person(
                username=parent.emplid,
                first_name=parent.first_name,
                last_name=parent.last_name,
                email=parent.emailAddress,
            )
            print lec, newLEC, oldPerson


class Lecturer(Person):

    subjects = models.ManyToManyField('Subject')
    courses = models.ManyToManyField('Course')
    objects = LecturerManager()

    class Meta:
        verbose_name = 'lecturer'
        verbose_name_plural = 'lecturers'


# class Professor(Instructor):
#
#     class Meta:
#         verbose_name = 'professor'
#         verbose_name_plural = 'faculty'
#
#     #department = models.ManyToManyField('Department')
#     title = models.CharField(max_length=128, blank=True, null=True)
#     level = models.CharField(max_length=16, blank=True, null=True, choices=(
#         ('ASST', 'Assistant Professor'),
#         ('ASSC','Associate Professor'),
#         ('FULL', 'Full Professor'),
#     ))

# class Staff(Instructor):
#
#     class Meta:
#         verbose_name = 'staff member'
#         verbose_name_plural = 'staff'
#
#     #department = models.ManyToManyField('Department')
#     title = models.CharField(max_length=128, blank=True, null=True)


class GTAParent(models.Model):

    emplid = models.CharField(max_length=11, db_column='EMPLID', primary_key=True)
    firstName = models.CharField(max_length=30, db_column='FIRST_NAME')
    lastName = models.CharField(max_length=30, db_column='LAST_NAME')
    emailAddress = models.CharField(max_length=30, db_column='EMAIL_ADDR')
    lastRegisteredTerm = models.CharField(max_length=4, db_column='STRM')
    cumulativeGPA = models.DecimalField(max_digits=4, decimal_places=2, db_column='CUM_GPA')

    class Meta:
        managed = False
        db_table = 'GTA'

    def __unicode__(self):
        return '{0}  {1}  {2} {3} {4}'.format(
            self.emplid, self.firstName, self.lastName, self.cumulativeGPA,
            self.lastRegisteredTerm
        )


class GTAManager(StudentManager):

    def get_or_create_with_student(self, **kwargs):
        newGTA = False
        oldStudent = False
        try:
            gta = self.get(username=kwargs['username'])
        except:
            newGTA = True
            try:
                gta = self.create(**kwargs)
                gta.save()
            except:
                oldStudent = True
                student = Student.objects.get(username=kwargs['username'])
                gta = self.create(student_ptr=student, gpa=kwargs['gpa'])
                gta.__dict__.update(student.__dict__)
                gta.save()
        return (gta, newGTA, oldStudent,)

    def update_from_employee_table(self):
        parents = GTAParent.objects.all()
        for parent in parents:
            gta, newGTA, oldStudent = self.get_or_create_with_student(
                username=parent.emplid,
                first_name=parent.firstName,
                last_name=parent.lastName,
                email=parent.emailAddress,
                gpa=parent.cumulativeGPA
            )
            print gta, newGTA, oldStudent

    def update_from_instructor_table(self):
        parents = InstructorParent.objects.filter(job='GTA')
        for parent in parents:
            gta, newGTA, oldStudent = self.get_or_create_with_student(
                username=parent.emplid,
                first_name=parent.first_name,
                last_name=parent.last_name,
                email=parent.emailAddress,
            )
            print gta, newGTA, oldStudent

class GTA(Student):

    gpa = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    objects = GTAManager()

    class Meta:
        verbose_name = 'GTA'
        verbose_name_plural = 'GTAs'


class FinancialDepartmentParent(models.Model):
    deptid = models.CharField(primary_key=True, max_length=20, db_column='DEPTID')
    dept_name = models.CharField(max_length=30, db_column='DEPT_NAME')
    college_deptid = models.CharField(max_length=20, db_column='COLLEGE_DEPTID')
    college_name = models.CharField(max_length=30, db_column='COLLEGE_NAME')
    cabinet_deptid = models.CharField(max_length=20, db_column='CABINET_DEPTID')
    cabinet_name = models.CharField(max_length=30, db_column='CABINET_NAME')
    cfs_dept_name = models.CharField(max_length=100, db_column='CFS_DEPT_NAME')
    acad_org = models.CharField(max_length=25, db_column='ACAD_ORG')
    acad_group = models.CharField(max_length=25, db_column='ACAD_GROUP')

    class Meta:
        managed = False
        db_table = 'DEPARTMENT_HIERARCHY_VW'


class FinancialDepartmentManager(models.Manager):

    def sync(self):
        parents = FinancialDepartmentParent.objects.all()
        for parent in parents:
            financialDepartment = self.get_or_create(deptID=parent.deptid,
                                                     deptName=parent.dept_name,
                                                     college_deptid=parent.college_deptid,
                                                     college_name=parent.college_name,
                                                     cabinet_deptid=parent.cabinet_deptid,
                                                     cfs_dept_name=parent.cfs_dept_name,
                                                     acad_org=parent.acad_org,
                                                     acad_group=parent.acad_group,
                                                     )


class FinancialDepartment(models.Model):
    deptID = models.CharField(max_length=20)
    deptName = models.CharField(max_length=60)
    college_deptid = models.CharField(max_length=20)
    college_name = models.CharField(max_length=60)
    cabinet_deptid = models.CharField(max_length=20)
    cabinet_name = models.CharField(max_length=60)
    cfs_dept_name = models.CharField(max_length=100)
    acad_org = models.CharField(max_length=25)
    acad_group = models.CharField(max_length=25)
    objects = FinancialDepartmentManager()

    def __unicode__(self):
        return self.deptName


class AcademicGroupParent(models.Model):
    deptID = models.CharField(max_length=20, db_column='DEPTID')
    deptName = models.CharField(max_length=30, db_column='DEPT_NAME')
    college_deptid = models.CharField(max_length=4, db_column='COLLEGE_DEPTID')
    college_name = models.CharField(max_length=100, db_column='COLLEGE_NAME')
    acad_group = models.CharField(primary_key=True, max_length=3, db_column='ACAD_GROUP')
    college_nickname = models.CharField(max_length=4, db_column='COLLEGE_NICKNAME')

    class Meta:
        managed = False
        db_table = 'COLLEGE_VW'


class AcademicGroupManager(models.Manager):

    def sync(self):
        parents = AcademicGroupParent.objects.all()
        for parent in parents:
            print parent.deptID
            try:
                financialDepartment = FinancialDepartment.objects.get(deptID=parent.deptID)
            except:
                print 'Financial Department does not yet exist'
                return
            try:
                acadGroup = self.get(financialDepartment=financialDepartment)
            except:
                acadGroup = AcademicGroup(name=parent.college_name,
                                           nickname = parent.college_nickname,
                                           number = parent.acad_group,
                                           financialDepartment = financialDepartment,
                                           )
                acadGroup.save()


class AcademicGroup(models.Model):
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=60, blank=True, null=True)
    number = models.CharField(max_length=5, blank=True, null=True)
    financialDepartment = models.ForeignKey(FinancialDepartment, blank=True, null=True)
    objects = AcademicGroupManager()
    #admins = models.ManyToManyField(Person, related_name='academic_groups_as_admin', blank=True)

    def __unicode__(self):
        return self.name


class AcademicOrganizationParent(models.Model):
    acad_org = models.CharField(primary_key=True ,max_length=10, db_column='ACAD_ORG')
    deptID = models.CharField(max_length=20, db_column='DEPTID')
    deptName = models.CharField(max_length=30, db_column='DEPT_NAME')
    acad_group = models.CharField(max_length=3, db_column='ACAD_GROUP')

    class Meta:
        managed = False
        db_table = 'DEPARTMENT_VW'


class AcademicOrganizationManager(models.Manager):

# todo Handle exceptions
# todo edit DEPARTMENT_HIERARCHY view to get 131 - *

    def sync(self):
        parents = AcademicOrganizationParent.objects.all()
        for parent in parents:
            print parent.acad_org
            try:
                financialDepartment = FinancialDepartment.objects.get(deptID=parent.deptID)
            except:
                print 'Financial Department does not yet exist'
                financialDepartment = None
            try:
                acadGroup = AcademicGroup.objects.get(number=parent.acad_group)
            except:
                print 'Academic Group does not yet exist'
                acadGroup = None
            try:
                acadOrg = self.get(acad_org=parent.acad_org)
            except:
                acadOrg = AcademicOrganization(name=parent.deptName,
                                               acad_org=parent.acad_org,
                                               academicGroup=acadGroup,
                                               financialDepartment=financialDepartment,
                                               )
                acadOrg.save()


class AcademicOrganization(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)
    nickname = models.CharField(max_length=32, blank=True, null=True)
    acad_org = models.CharField(max_length=10, blank=True, null=True)
    academicGroup = models.ForeignKey(AcademicGroup, blank=True, null=True)
    financialDepartment = models.ForeignKey(FinancialDepartment, blank=True, null=True)
    objects = AcademicOrganizationManager()

    def __unicode__(self):
        return self.acad_org

    def TTSFR(self, termNumber):
        #people = Person.objects.filter(acad_org=self, term__number=termNumber)
        sections = Section.objects.filter(session__course__subject__host=self,
                                          session__term__number=termNumber)
        # 7/22/2019 Change to self.section_set.filter(session__term__number=termNumber)
        ftes = 0.
        for section in sections:
            ftes += section.FTES()
        return ftes

        # ftef = 0.
        # for person in people:
        #     if person.jobcode = 'TEN':
        #         ftef += person.fte


class College(AcademicGroup):
    dean = models.ForeignKey(Person, related_name='colleges_is_dean', blank=True, null=True)
    #staff = models.ManyToManyField(Person, related_name='colleges_is_staff', blank=True)


class School(AcademicOrganization):
    college = models.ForeignKey(College)
    director = models.ForeignKey(Person, related_name='schools_is_director', blank=True, null=True)
    aoc = models.ForeignKey(Person, related_name='schools_is_aoc', blank=True, null=True)


class Department(AcademicOrganization):
    college = models.ForeignKey(College)
    chair = models.ForeignKey(Person, related_name='departments_is_chair', blank=True, null=True)
    aoc = models.ForeignKey(Person, related_name='departments_is_aoc', blank=True, null=True)
    #staff = models.ManyToManyField(Person, related_name='departments_is_staff', blank=True)
    #faculty = models.ManyToManyField(Person, related_name='departments_is_faculty', blank=True)


class Program(AcademicOrganization):
    college = models.ForeignKey(College)
    director = models.ForeignKey(Person, related_name='programs_is_director', blank=True, null=True)
    aoc = models.ForeignKey(Person, related_name='programs_is_aoc', blank=True, null=True)


class Subject(models.Model):
    name = models.CharField(max_length=8, unique=True)
    description = models.CharField(max_length=60, blank=True, null=True)
    host = models.ForeignKey(AcademicOrganization, blank=True, null=True)

    def __unicode__(self):
        return self.name

    def get_by_natural_key(self, subjectName):
        return self.get(name=subjectName)

    def natural_key(self):
        return (self.name,)


class Component(models.Model):
    name = models.CharField(max_length=8)
    description = models.CharField(max_length=60, blank=True, null=True)

    def __unicode__(self):
        return self.name


class CourseComponent(models.Model):
    course = models.ForeignKey('Course')
    component = models.ForeignKey(Component)
    units = models.SmallIntegerField()

    def __unicode__(self):
        return self.name


class GradingBasis(models.Model):
    choice = models.CharField(max_length=3, choices=(
        ('OPT','Plus/Minus Letter or CR/NC'),
        ('GRD', 'Plus/Minus Letter'),
        ('CNC', 'Credit / No-Credit'),
        ('SFQ', 'Plus/Minus ABC/NC'),
        ('SFW', 'ABC/NC'),
        ('SFJ', 'Plus/Minus AB/NC'),
        ('SFG', 'SFG: Grad supervision, allows RP'),
        ('SFI', 'SFI: Grad supervision, allows RP'),
        ('CEU', 'CEL'),
        ('NOG', 'Non graded (culminating experience)'),
        ('NON', 'Non-graded section of multisection class'),
        ('ADM', 'Administratively Determined'),
        ('AUD', 'Audit')
    ))
    # plusMinus = models.BooleanField()
    # letters = models.CharField(max_length=5)
    # credit = models.BooleanField()
    # noCredit = models.BooleanField()
    # reportProgress = models.BooleanField()
    #
    # def convert(self, toGradingBasis, academicCareer):


    class Meta:
        verbose_name_plural = "Grading Bases"

    def __unicode__(self):
        return self.choice


class KFactorManager(models.Manager):

    def WTUperSCU(self, aCSNumber):
        try:
            kfactor = self.get(CSNumber=aCSNumber)
            return kfactor.factor
        except:
            return None


class KFactor(models.Model):
    CSNumber = models.SmallIntegerField(blank=True, null=True)
    factor = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    objects = KFactorManager()

    def __unicode__(self):
        return 'KFactor({0}) = {1}'.format(self.CSNumber, self.factor)


class CourseParent(models.Model):
    crse_id = models.CharField(max_length=6, db_column='CRSE_ID', primary_key=True)
    effdt = models.DateField(db_column='EFFDT')
    eff_status = models.CharField(max_length=1, db_column='EFF_STATUS')
    course_title_long = models.CharField(max_length=100, db_column='COURSE_TITLE_LONG')
    descrlong = models.CharField(max_length=4000, db_column='DESCRLONG')
    component_primary = models.CharField(max_length=3, db_column='COMPONENT_PRIMARY')
    units_acad_prog = models.SmallIntegerField(db_column='UNITS_ACAD_PROG')
    crse_contact_hrs = models.SmallIntegerField(db_column='CRSE_CONTACT_HRS')
    fees_exist = models.CharField(max_length=1, db_column='FEES_EXIST')
    crse_offer_nbr = models.IntegerField()
    subject = models.CharField(max_length=8, db_column='SUBJECT')
    catalog_nbr = models.CharField(max_length=10, db_column='CATALOG_NBR')
    acad_group = models.CharField(max_length=5, db_column='ACAD_GROUP')
    acad_org = models.CharField(max_length=10, db_column='ACAD_ORG')
    acad_career = models.CharField(max_length=4, db_column='ACAD_CAREER')

    class Meta:
        managed = False
        db_table = 'CURRENT_COURSE_VW'


class CourseManager(models.Manager):

    def sync(self, **kwargs):
        parents = CourseParent.objects.filter(**kwargs)
        for parent in parents:
            try:
                course = self.get(
                    subject__name=parent.subject.strip(),
                    number=parent.catalog_nbr.strip(),
                    courseID=parent.crse_id.strip(),
                )
                course.effectiveDate = parent.effdt
                course.effectiveStatus = parent.eff_status
                course.title = parent.course_title_long.encode('ascii','replace').strip()
                course.description = parent.descrlong.encode('ascii','replace').strip()
                course.unitsAcadProg = parent.units_acad_prog
                course.contactHours = parent.crse_contact_hrs
                course.offerNumber = parent.crse_offer_nbr
                course.academicCareer = parent.acad_career
            except:
                subject, new = Subject.objects.get_or_create(
                    name=parent.subject.strip()
                )
                if new:
                    host, new = AcademicOrganization.objects.get_or_create(
                        acad_org=parent.acad_org.strip()
                    )
                    subject.host = host
                    subject.save()
                course = self.create(
                    subject=subject,
                    number=parent.catalog_nbr.strip(),
                    courseID=parent.crse_id.strip(),
                    effectiveDate=parent.effdt,
                    effectiveStatus=parent.eff_status,
                    title=parent.course_title_long.encode('ascii','replace').strip(),
                    description=parent.descrlong.encode('ascii','replace').strip(),
                    unitsAcadProg=parent.units_acad_prog,
                    contactHours=parent.crse_contact_hrs,
                    offerNumber=parent.crse_offer_nbr,
                )
            try:
                course.academicOrganization = AcademicOrganization.objects.get(
                    acad_org=parent.acad_org
                )
            except:
                print 'ACAD ORG: ' + parent.acad_org + ' does not yet exist'
            try:
                course.academicGroup = AcademicGroup.objects.get(
                    number=parent.acad_group
                )
            except:
                print 'ACAD GROUP: ' + parent.acad_group + ' does not yet exist'
            course.save()


class Course(models.Model):
    subject = models.ForeignKey(Subject)
    number = models.CharField(max_length=8)
    courseID = models.CharField(max_length=6)
    effectiveDate = models.DateTimeField()
    effectiveStatus = models.CharField(max_length=1)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=4000)
    components = models.ManyToManyField('Component', through='CourseComponent', blank=True)
    gradingBasis = models.ManyToManyField('GradingBasis', blank=True)
    unitsAcadProg = models.SmallIntegerField()
    contactHours = models.SmallIntegerField()
    offerNumber = models.IntegerField()
    academicOrganization = models.ForeignKey(AcademicOrganization, blank=True, null=True)
    academicGroup = models.ForeignKey(AcademicGroup, blank=True, null=True)
    academicCareer = models.CharField(max_length=4)
    attributes = models.ManyToManyField('CourseAttribute', blank=True)
    cadence = models.ForeignKey('Cadence', blank=True, null=True)
    prerequisites = models.ManyToManyField('self', blank=True,
                                           symmetrical=False,
                                           through='Prerequisite',
                                           related_name='prerequisites_to')
    corequisites = models.ManyToManyField('self', blank=True,
                                          symmetrical=False,
                                          related_name='corequisites_to')
    # entranceExams = models.ManyToManyField('Exam', blank=True)
    studentGrades = models.ManyToManyField(Student, blank=True,
                                           through='StudentGrade',
                                           related_name='courseGrades'
                                           )
    objects = CourseManager()

    class Meta:
        unique_together = (('subject', 'number', 'courseID'),)

    def __unicode__(self):
        return "{0} {1}    {2}".format(self.subject.__unicode__(),
                                       self.number,
                                       self.title
                                       )

    def units(self):
        units = 0
        components = self.components.all()
        if components:
            for component in components:
                units += component.units
        else:
            units = self.unitsAcadProg
        return units

    def parsePrerequisites(self):
        courseStrings = re.findall(self.description, '[\s\w]{4}[\s\d]{4}')
        for courseString in courseStrings:
            print courseString


class CourseAttributeParent(models.Model):
    crse_attr = models.CharField(max_length=4, db_column='CRSE_ATTR', primary_key=True)
    crse_attr_value = models.CharField(max_length=10, db_column='CRSE_ATTR_VALUE')
    descr = models.CharField(max_length=30, db_column='DESCR')
    descrformal = models.CharField(max_length=50, db_column='DESCRFORMAL')

    class Meta:
        managed = False
        db_table = 'COURSE_ATTRIBUTE_VW'


class CourseAttributeManager(models.Manager):

    def sync(self, **kwargs):
        parents = CourseAttributeParent.objects.filter(**kwargs)
        for parent in parents:
            attr = self.get_or_create(
                name=parent.crse_attr.strip(),
                value=parent.crse_attr_value.strip(),
                description = parent.descrformal.strip(),
            )


class CourseAttribute(models.Model):
    name = models.CharField(max_length=4, blank=True)
    value = models.CharField(max_length=10, blank=True)
    description = models.CharField(max_length=50, blank=True)
    objects = CourseAttributeManager()

    def __unicode__(self):
        if all(ord(char) < 128 for char in self.description):
            return '{0}: {1} {2}'.format(self.name, self.value, self.description)
        else:
            return '{0}: {1}'.format(self.name, self.value)

class Cadence(models.Model):
    terms = models.CharField(max_length=30, blank=True)
    years = models.CharField(max_length=30, blank=True)

    def check_term(self, term):
        pass #if term meets cadence conditions return True

    def __unicode__(self):
        return '{0} terms in {1} years'.format(self.terms, self.years)



# TODO parse prerequisites from text to course objects
class Prerequisite(models.Model):
    requiredForCourse = models.ForeignKey(Course,
                                          related_name='coursesWithPrerequisites')
    requiredCourse = models.ForeignKey(Course,
                                       related_name='prerequisiteCourses')
    gradeList = sorted(list(Grade(i) for i in Grade.validGrades.keys()),
                       reverse=True)
    choices = tuple(tuple([i, i]) for i in gradeList)
    passingGrade = GradeField(choices=choices, blank=True)

    def __unicode__(self):
        s = self.requiredForCourse.__unicode__() + ' requires '
        s += self.get_passingGrade_display() + ' or better in '
        s += self.requiredCourse.__unicode__()
        return s




class StudentGrade(models.Model):
    course = models.ForeignKey(Course)
    student = models.ForeignKey(Student)
    gradeList = sorted(list(Grade(i) for i in Grade.validGrades.keys()),
                       reverse=True)
    choices = tuple(tuple([i, i]) for i in gradeList)
    grade = GradeField(blank=True)

    def __unicode__(self):
        s = self.student
        return s.firstName + ' ' + s.lastName + ' has ' + \
               self.grade.letterGrade + ' in ' + self.course.__unicode__()


class TermParent(models.Model):
    strm = models.CharField(max_length=4, db_column='STRM', primary_key=True)
    descr = models.CharField(max_length=30, db_column='DESCR')
    descrshort = models.CharField(max_length=10, db_column='DESCRSHORT')
    term_begin_dt = models.DateField(db_column='TERM_BEGIN_DT')
    term_end_dt = models.DateField(db_column='TERM_END_DT')
    session_code = models.CharField(max_length=3, db_column='SESSION_CODE')
    weeks_of_instruct = models.IntegerField(db_column='WEEKS_OF_INSTRUCT')
    term_category = models.CharField(max_length=1, db_column='TERM_CATEGORY')
    acad_year = models.CharField(max_length=4, db_column='ACAD_YEAR')

    class Meta:
        managed = False
        db_table = '"CMSCOMMON"."SFO_TERM_TBL"'

    def __unicode__(self):
        return self.descr


class TermManager(models.Manager):

    def get_or_create_from_number(self, number):
        year = '{0}0{1}'.format(number[0], number[1:3])
        season = number[3]
        return self.get_or_create(season=season, year=year)

    def sync(self):

        termParents = TermParent.objects.all()

        for termParent in termParents:
            try:
                term = self.get(
                    term__number=termParent.strm,
                )
            except:
                term, new = Term.objects.get_or_create_from_number(
                    termParent.strm
                )
                print term, new
            term.startDate = termParent.term_begin_dt
            term.endDate = termParent.term_end_dt
            term.descr = termParent.descr
            term.descrshort = termParent.descrshort
            term.sessionCode = termParent.session_code
            term.weeksOfInstruct = termParent.weeks_of_instruct
            term.termCategory = termParent.term_category
            term.academicYear = termParent.acad_year
            term.save()



class Term(models.Model):
    season = models.CharField(max_length=20,
                              choices=(('1', 'Winter'),
                                       ('3', 'Spring'),
                                       ('5', 'Summer'),
                                       ('7', 'Fall'),
                              )
    )
    year = models.CharField(max_length=4)
    number = models.CharField(max_length=4, unique=True)
    startDate = models.DateField(blank=True, null=True)
    endDate = models.DateField(blank=True, null=True)
    descr = models.CharField(max_length=30, blank=True, null=True)
    descrshort = models.CharField(max_length=10, blank=True, null=True)
    sessionCode = models.CharField(max_length=3, blank=True, null=True)
    weeksOfInstruct = models.IntegerField(blank=True, null=True)
    termCategory = models.CharField(max_length=1, blank=True, null=True)
    academicYear = models.CharField(max_length=4, blank=True, null=True)
    instructors = models.ManyToManyField('Person', blank=True, through='TermInstructor')
    objects = TermManager()

    def _number(self):
        return ''.join(re.search('(\d)\d(\d{2})',
                                 self.year).groups()) + self.season

    def clean(self):
        self.number = self._number()

    def save(self, *args, **kwargs):
        self.clean()
        super(Term, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.get_season_display() + self.year

    def snap(self):
        EnrollmentSnapshot.objects.snap(self)


class EnrollmentSnapshotManager(models.Manager):

    def snap(self, term):
        sections = Section.objects.filter(session__term=term)
        for section in sections:
            enrollmentSnapshot=self.create(section=section,
                                                  date=datetime.datetime.now(),
                                                  enrollCap=section.enrollCap,
                                                  enrolled=section.enrolled,
                                                  waitlistCap=section.waitlistCap,
                                                  waitlisted=section.waitlised)


class EnrollmentSnapshot(models.Model):
    section = models.ForeignKey('Section')
    date = models.DateTimeField(auto_now=True)
    enrollCap = models.SmallIntegerField()
    enrolled = models.SmallIntegerField()
    waitlistCap = models.SmallIntegerField()
    waitlisted = models.SmallIntegerField()
    objects = EnrollmentSnapshotManager()


class SessionCorrelation(models.Model):

    fromSession = models.ForeignKey('Session',related_name='from_correlations')
    toSession = models.ForeignKey('Session', related_name='to_correlations')
    coefficient = models.FloatField()

    def __unicode__(self):
        return '{0}, {1}: {2}'.format(self.fromSession, self.toSession, self.coefficient)


class SessionConflict(models.Model):

    fromSession = models.ForeignKey('Session', related_name='from_conflicts')
    toSession = models.ForeignKey('Session', related_name='to_conflicts')
    seats = models.IntegerField()


class SessionManager(models.Manager):

    def sync(self):

        parents = SectionParent.objects.all()   # SectionParent unmanaged model is correct!!!!!!

        for parent in parents:
            try:
                session = self.get(
                    term__number=parent.strm.strip(),
                    course__subject__name=parent.subject.strip(),
                    course__number=courseNumber.strip()
                )
            except:
                term, new = Term.objects.get_or_create_from_number(parent.strm.strip())
                print term
                subject, new = Subject.objects.get_or_create(name=parent.subject.strip())
                print subject
                course, new = Course.objects.get_or_create(
                    subject=subject,
                    number=parent.catalogNumber.strip()
                )
                print course
                session, new = self.get_or_create(term=term, course=course)
                if new:
                    print session, ' NEW'
                else:
                    print session


class Session(models.Model):
    course = models.ForeignKey(Course)
    term = models.ForeignKey(Term)
    coordinator = models.ForeignKey(Person, blank=True, null=True)
    correlations = models.ManyToManyField('self', symmetrical=False,
                                          through='SessionCorrelation',
                                          related_name='correlated_with')
    conflicts = models.ManyToManyField('self', symmetrical=False,
                                       through='SessionConflict',
                                       related_name='conflicts_with')
    objects = SessionManager()

    def __unicode__(self):
        return "{0}  {1}".format(self.course.__unicode__(),
                                 self.term.__unicode__())

    class Meta:
        unique_together = (('course', 'term'),)

    def conflictedSeats(self, other):
        if not isinstance(other, Session):
            raise
        seats = 0
        for section in self.section_set:
            unassignedSeats = section.enrollCap
            for otherSection in other.section_set:
                if section.conflictsWith(otherSection):
                    return
                else:
                    unassignedSeats -= otherSection.enrollCap

    def sessionCap(self):
        cap = 0
        for section in self.section_set:
            cap += section.enrollCap
        return cap


class ParentRouter(object):

    def db_for_read(self, model, **hints):
        if model._meta.managed==False:
            return 'parent'
        return None

class SectionParent(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID')
    institution = models.CharField(max_length=5, db_column='INSTITUTION')
    strm = models.CharField(max_length=4, db_column='STRM')
    courseID = models.CharField(max_length=6, db_column='CRSE_ID')
    sessionCode = models.CharField(max_length=3, db_column='SESSION_CODE')
    courseOfferNumber = models.IntegerField(db_column='CRSE_OFFER_NBR')
    classSection = models.CharField(max_length=4, db_column='CLASS_SECTION')
    classNumber = models.IntegerField(db_column='CLASS_NBR')
    acadGroup = models.CharField(max_length=5, db_column='ACAD_GROUP')
    acadOrg = models.CharField(max_length=10, db_column='ACAD_ORG')
    subject = models.CharField(max_length=8, db_column='SUBJECT')
    catalogNumber = models.CharField(max_length=10, db_column='CATALOG_NBR')
    associatedClass = models.IntegerField(db_column='ASSOCIATED_CLASS')
    autoEnrollSect1 = models.CharField(max_length=4, db_column='AUTO_ENROLL_SECT_1')
    courseDescription = models.CharField(max_length=30, db_column='DESCR')
    courseTopicID = models.IntegerField(db_column='CRS_TOPIC_ID')
    classMeetingNumber = models.IntegerField(db_column='CLASS_MTG_NBR')
    csuCOCSNumber = models.CharField(max_length=2, db_column='CSU_CO_CS_NUMBER')
    courseComponent = models.CharField(max_length=3, db_column='SSR_COMPONENT')
    studentCreditUnits = models.IntegerField(db_column='CSU_APDB_CMP_UNITS')
    tbaHours = models.DecimalField(max_digits=5, decimal_places=2, db_column='CSU_APDB_TBA_HOURS')
    learningMode = models.CharField(max_length=2, db_column='CSU_APDB_LRNG_MODE')
    startDate = models.DateTimeField(db_column='START_DATE')
    endDate = models.DateTimeField(db_column='END_DATE')
    facilityID = models.CharField(max_length=10, db_column='FACILITY_ID')
    standardMeetingPattern = models.CharField(max_length=4, db_column='STND_MTG_PAT')
    meetingTimeStart = models.DateTimeField(db_column='MEETING_TIME_START')
    meetingTimeEnd = models.DateTimeField(db_column='MEETING_TIME_END')
    enrollCap = models.IntegerField(db_column='ENRL_CAP')
    enrollTotal = models.IntegerField(db_column='ENRL_TOT')
    waitCap = models.IntegerField(db_column='WAIT_CAP')
    waitTotal = models.IntegerField(db_column='WAIT_TOT')
    instructorLastName = models.CharField(max_length=30, db_column='LAST_NAME')
    instructorFirstName = models.CharField(max_length=30, db_column='FIRST_NAME')
    instructorID = models.CharField(max_length=9, db_column='EMPLID')
    schedulePrint = models.CharField(max_length=1, db_column='SCHEDULE_PRINT')
    classStatus = models.CharField(max_length=1, db_column='CLASS_STAT')
    enrollStatus = models.CharField(max_length=1, db_column='ENRL_STAT')
    classType = models.CharField(max_length=1, db_column='CLASS_TYPE')
    acadCareer = models.CharField(max_length=4, db_column='ACAD_CAREER')
    sectionCombinedID = models.CharField(max_length=4, db_column='SCTN_COMBINED_ID')
    minimumUnits = models.IntegerField(db_column='UNITS_MINIMUM')
    maximumUnits = models.IntegerField(db_column='UNITS_MAXIMUM')
    instructorAssignSequence = models.IntegerField(db_column='INSTR_ASSIGN_SEQ')
    instructorLoadFactor = models.IntegerField(db_column='INSTR_LOAD_FACTOR')
    schedulePrintInstructor = models.CharField(max_length=1, db_column='SCHED_PRINT_INSTR')
    instructorRole = models.CharField(max_length=4, db_column='INSTR_ROLE')
    employeeRecord = models.IntegerField(db_column='EMPL_RCD')
    sfoCourseTopicTL = models.CharField(max_length=30, db_column='SFO_CRSE_TPC_TL')
    classNoteNumber = models.CharField(max_length=4, db_column='CLASS_NOTE_NBR')
    fte = models.DecimalField(max_digits=5, decimal_places=2, db_column='SFO_OSB_FTE')
    departmentName = models.CharField(max_length=30, db_column='SFO_DEPT_NAME')
    jobCode = models.CharField(max_length=6, db_column='JOBCODE')
    roomCharacteristic = models.CharField(max_length=2, db_column='ROOM_CHRSTC')
    weekWorkloadHours = models.IntegerField(db_column='WEEK_WORKLOAD_HRS')
    generalAssign = models.CharField(max_length=1, db_column='GENERL_ASSIGN')

    class Meta:
        managed = False
        db_table = 'SFO_CS_OSB1_VW'

    def __unicode__(self):
        return "{0} {1}{2}.{3}".format(self.strm, self.subject,
                                 self.catalogNumber,
                                  self.classSection)



class DeprecatedSectionParent(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID')
    strm = models.CharField(max_length=4, db_column='STRM')
    classNumber = models.IntegerField(db_column='CLASS_NBR')
    courseID = models.CharField(max_length=6, db_column='CRSE_ID')
    subject = models.CharField(max_length=8, db_column='SUBJECT')
    catalogNumber = models.CharField(max_length=10, db_column='CATALOG_NBR')
    classSection = models.CharField(max_length=4, db_column='CLASS_SECTION')
    courseDescription = models.CharField(max_length=30, db_column='DESCR')
    units = models.IntegerField(db_column='UNITS_ACAD_PROG')
    courseType = models.CharField(max_length=3, db_column='SSR_COMPONENT')
    meetDays = models.CharField(max_length=4, db_column='MEETING_DAYS')
    startTime = models.CharField(max_length=5, db_column='START_TIME')
    endTime = models.CharField(max_length=5, db_column='END_TIME')
    startDate = models.CharField(max_length=11, db_column='START_DATE')
    endDate = models.CharField(max_length=11, db_column='END_DATE')
    building = models.CharField(max_length=10, db_column='BLDG_CD')
    room = models.CharField(max_length=10, db_column='ROOM')
    enrollCap = models.IntegerField(db_column='ENRL_CAP')
    waitCap = models.IntegerField(db_column='WAIT_CAP')
    instructorID = models.CharField(max_length=9, db_column='EMPLID')
    instructorFirstName = models.CharField(max_length=30, db_column='FIRST_NAME')
    instructorLastName = models.CharField(max_length=30, db_column='LAST_NAME')
    instructorEmail = models.CharField(max_length=40, db_column='EMAIL_ADDR')
    enrollCount = models.IntegerField(db_column='ENRL_TOT')
    waitCount = models.IntegerField(db_column='WAIT_TOT')
    enrollingStatus = models.CharField(max_length=1, db_column='ENRL_STAT')
    classStatus = models.CharField(max_length=1, db_column='CLASS_STAT')
    classType = models.CharField(max_length=1, db_column='CLASS_TYPE')
    associatedClass = models.IntegerField(db_column='ASSOCIATED_CLASS')
    schedulePrint = models.CharField(max_length=1, db_column='SCHEDULE_PRINT')
    acadOrg = models.CharField(max_length=10, db_column='ACAD_ORG')
    acadCareer = models.CharField(max_length=4, db_column='ACAD_CAREER')
    acadGroup = models.CharField(max_length=5, db_column='ACAD_GROUP')
    institution = models.CharField(max_length=5, db_column='INSTITUTION')
    campus = models.CharField(max_length=5, db_column='CAMPUS')
    campusEventNumber = models.CharField(max_length=9, db_column='CAMPUS_EVENT_NBR')
    combinedSection = models.CharField(max_length=1, db_column='COMBINED_SECTION')
    sessionCode = models.CharField(max_length=3, db_column='SESSION_CODE')



    class Meta:
        managed = False
        db_table = 'SECTION_VW'

    def __unicode__(self):
        return "{0} {1}{2}.{3}".format(self.strm, self.subject,
                                 self.catalogNumber,
                                  self.classSection)

class SectionManager(models.Manager):

    def sync(self, user):

        #if unit in acadGroups:
        #    sectionParents = SectionParent.objects.filter(acadGroup=unit)
        #if unit
        sectionParents = SectionParent.objects.all()

        for sectionParent in sectionParents:
            try:
                section = self.get(
                    session__term__number=sectionParent.strm.strip(),
                    session__course__subject__name=sectionParent.subject.strip(),
                    session__course__number=sectionParent.catalogNumber.strip(),
                    number=sectionParent.classSection.strip(),
                    classNumber=sectionParent.classNumber
                )
            except:
                term, new = Term.objects.get_or_create_from_number(
                    sectionParent.strm.strip()
                )
                if new:
                    term.startDate = sectionParent.startDate.date()
                    term.endDate = sectionParent.endDate.date()
                    term.save()
                print term, new
                subject, new = Subject.objects.get_or_create(
                    name=sectionParent.subject.strip()
                )
                print subject, new
                courseComponent, new = CourseComponent.objects.get_or_create(
                    name=sectionParent.courseComponent)
                course, new = Course.objects.get_or_create(
                    subject=subject,
                    number=sectionParent.catalogNumber.strip(),
                    #courseType = courseType
                    # title=sectionParent.courseDescription.strip()
                )
                print course, new
                session, new = Session.objects.get_or_create(term=term, course=course)
                print session, new

                instructorExists = re.search('.', sectionParent.instructorID)
                if instructorExists:
                    instructor, new = Person.objects.get_or_create(
                        username=sectionParent.instructorID
                    )
                    if new:
                        TermInstructor.objects.create(
                            term=term,
                            instructor=instructor
                        )
                        #print 'sectionParent.instructorFirstName: ',sectionParent.instructorFirstName.strip()
                        instructor.first_name = sectionParent.instructorFirstName.strip()
                        instructor.last_name = sectionParent.instructorLastName.strip()
                        instructor.email = sectionParent.instructorEmail.strip()
                        #print 'instructor before save: ', instructor.first_name, instructor.last_name, instructor.username
                        instructor.save()
                if instructorExists:
                    print instructor.__unicode__().encode('ascii','replace')
                else:
                    print 'No istructor listed'
                print session,sectionParent.classSection.strip(),sectionParent.classNumber,courseType
                section, new = self.get_or_create(
                    session=session,
                    number=sectionParent.classSection.strip(),
                    classNumber=sectionParent.classNumber,
                    courseType=courseType
                )
                #if sectionParent.courseType is not None:
                #    section.courseType = sectionParent.courseType
                if instructorExists:
                    section.instructor = instructor
                #section.save()

                days = re.findall('[MTWRF]', sectionParent.meetDays)
                try:
                    startTime = datetime.datetime.strptime(sectionParent.startTime,'%H:%M')
                    endTime = datetime.datetime.strptime(sectionParent.endTime,'%H:%M')
                    date = endTime.date()
                    earliestStart = datetime.datetime.combine(date, datetime.time(hour=8))
                    earliestEnd = datetime.datetime.combine(date, datetime.time(hour=9, minute=45))
                    if startTime < earliestStart:
                        startTime += datetime.timedelta(hours=12)
                    if endTime < earliestEnd:
                        endTime += datetime.timedelta(hours=12)
                    for day in days:
                        meeting, new = WeeklyEvent.objects.get_or_create(
                            day=day,
                            startTime=startTime.time(),
                            endTime=endTime.time()
                        )
                        print day, startTime, endTime
                        #print meeting
                        #print section.meetings
                        section.meetings.add(meeting)
                except:
                    print 'No scheduled meeting time'

                if sectionParent.meetDays is not None and re.match('.', sectionParent.meetDays):
                    section.meetDays = sectionParent.meetDays
                if sectionParent.startTime is not None and re.match('.', sectionParent.startTime):
                    section.startTime = startTime
                if sectionParent.endTime is not None and re.match('.', sectionParent.endTime):
                    section.endTime = endTime
                #if re.match('.', sectionParent.building) and re.match('.', sectionParent.room):
                #    section.room = sectionParent.building.strip() + sectionParent.room.strip()
                #section.roomCap = sectionParent.roomCap
                section.enrollCap = sectionParent.enrollCap
                section.waitCap = sectionParent.waitCap
                section.save()

    def getQuickConflicts(self, termNumber=''):
        sectionDict = Section.objects.filter(session__term__number=termNumber).exclude(
            courseType__name='SUP').prefetch_related('meetings','session__term'
        ).in_bulk()
        sections = sectionDict.values()
        nSections = len(sections)
        for i in range(nSections):
            print sections[i]
            for j in range(i+1,nSections):
                if sections[i].conflictsWith(sections[j]):
                    pass
                    #print sections[i], ' conflicts with ', sections[j]
                    #sections[i].conflicts.add(sections[j])

    def getConflicts(self, termNumber=''):
        sections = Section.objects.filter(session__term__number=termNumber).exclude(
            courseType__name='SUP').prefetch_related('meetings').order_by(
            'session__term__number','session__course__subject__name',
            'session__course__number', 'number'
        )
        nSections = sections.count()
        for i in range(nSections):
            for j in range(i+1,nSections):
                if sections[i].conflictsWith(sections[j]):
                    print sections[i], ' conflicts with ', sections[j]
                    sections[i].conflicts.add(sections[j])

    def getLDLabSections(self, termNumber=''):
        return Section.objects.filter(
            session__term__number=termNumber,
            session__course__number__lt=300,
            courseType__name='LAB'
        ).exclude(
            number__contains='Z'
        ).order_by(
            'session__course__subject__name',
            'session__course__number', 'number'
        )

    def getUDGradSections(self, termNumber=''):
        return Section.objects.filter(
            session__term__number=termNumber,
            session__course__number__ge=330
        ).exclude(
            number__contains='Z',
            courseType__name='SUP'
        ).order_by(
            'session__course__subject__name',
            'session__course__number', 'number'
        )

    def getSCIPSectionAssignments(self, file=''):
        scipSol = open(file, 'r')
        for line in scipSol:
            if not re.match('^x\$', line):
                continue
            lastName, sectionName = re.search('x\$(.*)\$(\w*\.\w*)', line).groups()
            lastName = re.sub('_',' ',lastName)
            print lastName, sectionName[0:4],sectionName[4:8],sectionName[8:11],sectionName[12:14]
            instructor = Person.objects.get(last_name=lastName)
            section = self.get(
                #instructor__last_name=lastName,
                session__term__number=sectionName[0:4],
                session__course__subject__name=sectionName[4:8],
                session__course__number=sectionName[8:11],
                number=sectionName[12:14]
            )
            if section.instructor != instructor:
                section.instructor = instructor
                section.save()

    def getAssignmentsFromExcel(self, file=''):
        if file=='':
            print "'Usage: getAssignmentsFromExcel file='example.xlsx'"
            return
        sheet = pd.read_excel(file, header=0)
        for i in range(31):
            firstName = sheet['First Name'][i]
            lastName = sheet['Last Name'][i]
            emplid = unicode(int(sheet['SFSU ID'][i]))
            instructorType = sheet['GTA/LEC'][i]
            person = Person.objects.get(username=emplid)
            #print person, firstName, lastName
            for j in range(61):
                sectionName = sheet.columns[j + 9]
                section = Section.objects.get(
                    session__course__subject__name=sectionName[0:4],
                    session__course__number=sectionName[5:8],
                    number=sectionName[9:11],
                    session__term__number='2183'
                )
                #print sectionName, section, sheet.iloc[i, j+9]
                if sheet.iloc[i, j+9] == 1:
                    print sectionName, ' instructor = ', person
                    section.instructor = person
                    section.save()
                #section = section[0]


    def assignmentsCSVByInstructor(self, outfile='', term='2183', type=''):

        # get lower division labs only
        sections = self.filter(
            session__term__number=term,
            session__course__number__lt=300,
            #session__course__subject__name='PHYS',
            courseType__name='LAB'
        ).order_by('instructor__last_name', 'instructor__first_name',
                   'session__course__subject__name',
                   'session__course__number',
                   'number')
        #if type != '':
        #    sections = sections.filter(
        #        courseType__name=type
        #    )
        oString = ''
        for section in sections:
            startTime = section.startTime.__str__()[0:5]
            endTime = section.endTime.__str__()[0:5]
            print section, section.meetDays
            meetDays = re.sub('Su', '', section.meetDays)
            meetDays = re.sub('\s', '', meetDays)
            if section.instructor:
                print section, section.instructor
                oString += '{0},{1},{2},{3},{4}{5}.{6},{7} {8} - {9}\n'.format(
                    section.instructor.username,
                    section.instructor.first_name, section.instructor.last_name,
                    section.instructor.email,
                    section.session.course.subject.name,
                    section.session.course.number, section.number,
                    meetDays, startTime, endTime
                )
            if outfile == '':
                print oString
            else:
                out = open(outfile, 'w')
                out.write(oString[:-1])
                out.close()

    def assignmentsToConstraints(self, outfile='', term='2177', type=''):
        sections = self.filter(
            session__term__number=term,
        ).order_by('instructor__last_name', 'instructor__first_name',
                   'session__course__subject__name',
                   'session__course__number',
                   'number')
        if type != '':
            sections = sections.filter(
                courseType__name=type
            )
        m = -1;
        oString = ''
        for section in sections:
            m += 1
            if section.instructor:
                print section, section.instructor
                oString += 'subto assigned{0}{1} do x["{0}","{2}"]==1;\n'.format(
                    section.instructor.last_name, m, section.__unicode__()
                )
            if outfile == '':
                print oString
            else:
                out = open(outfile, 'w')
                out.write(oString)
                out.close()


class SectionInstructor(models.Model):
    instructor = models.ForeignKey(Person)
    section = models.ForeignKey('Section')
    fraction = models.DecimalField(max_digits=3, decimal_places=2, default=1.0)
    role = models.CharField(max_length=4, blank=True, null=True)
    sequence = models.IntegerField(blank=True, null=True)
    wtu = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    schedulePrint = models.BooleanField(default=True)


class Section(models.Model):
    session = models.ForeignKey(Session)
    number = models.CharField(max_length=4)
    classNumber = models.IntegerField()
    courseComponent = models.ForeignKey(CourseComponent, blank=True, null=True)
    kFactor = models.ForeignKey(KFactor, blank=True, null=True)
    instructors = models.ManyToManyField(Person, blank=True, through='SectionInstructor',
                                         related_name='sections_as_instructor')
    meetings = models.ManyToManyField(WeeklyEvent, blank=True)
    meetDays = models.CharField(max_length=32, blank=True, null=True)
    startTime = models.TimeField(blank=True, null=True)
    endTime = models.TimeField(blank=True, null=True)
    room = models.CharField(max_length=32, blank=True, null=True)
    roomCap = models.IntegerField(blank=True, null=True)
    enrollCap = models.IntegerField(blank=True, null=True)
    waitCap = models.IntegerField(blank=True, null=True)

    enrollStatus = models.CharField(max_length=1, blank=True, null=True)
    classStatus = models.CharField(max_length=1, blank=True, null=True)
    classType = models.CharField(max_length=1, blank=True, null=True)
    associatedClass = models.IntegerField(blank=True, null=True)
    schedulePrint = models.CharField(max_length=1, blank=True, null=True)
    acadOrg = models.CharField(max_length=10, blank=True, null=True)
    acadCareer = models.CharField(max_length=4, blank=True, null=True)
    acadGroup = models.CharField(max_length=5, blank=True, null=True)
    institution = models.CharField(max_length=5, blank=True, null=True)
    campus = models.CharField(max_length=5, blank=True, null=True)
    campusEventNumber = models.CharField(max_length=9, blank=True, null=True)
    combinedSection = models.CharField(max_length=1, blank=True, null=True)
    sessionCode = models.CharField(max_length=3, blank=True, null=True)

    conflicts = models.ManyToManyField('self', blank=True)
    students = models.ManyToManyField(Student, blank=True,
                                      through='SectionStudent')
                                      #related_name='sections')
    objects = SectionManager()

    class Meta:
        unique_together = ('session', 'number', 'classStatus')

    def __unicode__(self):
        return "{0}{1}{2}.{3}".format(
            self.session.term.number, self.session.course.subject.name,
            self.session.course.number, self.number
        )

    def getEnrolledStudents(self):
        return self.sectionstudent_set.filter(status='ENROLLED')

    def getWaitlistedStudents(self):
        return self.sectionstudent_set.filter(status='WAITLISTED')

    def getUnregisteredStudents(self):
        return self.sectionstudent_set.filter(status='UNREGISTERED')

    def getDroppedStudents(self):
        return self.sectionstudent_set.filter(status='DROPPED')

    def countEnrolledStudents(self):
        return self.getEnrolledStudents().count()

    def countWaitlistedStudents(self):
        return self.getWaitlistedStudents().count()

    def countUnregisteredStudents(self):
        return self.getUnregisteredStudents().count()

    def projectedEnrollmentWTU(self):
        return float(self.enrollCap >= 100)

    def actualEnrollmentWTU(self):
        return float(self.countEnrolledStudents() >= 100)

    def projectedWTU(self):
        return self.kFactor * self.session.course.units() + self.projectedEnrollmentWTU()

    def actualWTU(self):
        return self.session.course.units() * self.kFactor + self.actualEnrollmentWTU()

    def projectedCost(self):
        cost = 0.
        for instructor in self.instructors:
            cost += instructor.semesterSalaryForWTU(self.projectedWTU())
        return cost

    def actualCost(self):
        cost = 0.
        for instructor in self.instructors:
            cost += instructor.semesterSalaryForWTU(self.actualWTU)
        return cost

    def FTES(self):
        if self.acadCareer == 'UGRD':
            return self.session.course.units() * self.countEnrolledStudents()/15.
        else:
            return self.session.course.units() * self.countEnrolledStudents()/12.


    def conflictsWith(self, other):
        if isinstance(other, Section):
            if self == other:
                return False
            if self.session.term != other.session.term:
                return False
            if self.meetings.count() == 0 or other.meetings.count() == 0:
                return False
            #for meeting1 in self.meetings.all():
            #    for meeting2 in other.meetings.all():
            #        if meeting1.conflictsWith(meeting2):
            #            return True
            return False
        else:
            raise


class SectionStudentParent(models.Model):

    # from view that includes SFO_CR_ENROLL_VW and SFO_CR_MAIN_VW (for user info)

    sectionid = models.IntegerField(db_column='ID')
    strm = models.CharField(max_length=4, db_column='STRM')
    classNumber = models.IntegerField(db_column='CLASS_NBR')
    status = models.CharField(max_length=8, db_column='STATUS')
    enrolledStatus = models.CharField(max_length=8, db_column='ENROLLED_STATUS')
    subject = models.CharField(max_length=8, db_column='SUBJECT')
    catalogNumber = models.CharField(max_length=10, db_column='CATALOG_NBR')
    sessionCode = models.CharField(max_length=3, db_column='SESSION_CODE')
    classSection = models.CharField(max_length=4, db_column='CLASS_SECTION')
    username = models.CharField(max_length=11, db_column='EMPLID')
    first_name = models.CharField(max_length=30, db_column='FIRST_NAME')
    last_name = models.CharField(max_length=30, db_column='LAST_NAME')
    email = models.CharField(max_length=40, db_column='EMAIL_ADDR')
    academicPlan = models.CharField(max_length=10, db_column='ACAD_PLAN')
    academicPlanDescription = models.CharField(max_length=30, db_column='DESCR')
    academicLevel = models.CharField(max_length=3, db_column='ACAD_LEVEL_BOT')
    classLevel = models.CharField(max_length=10, db_column='CLASS_LEVEL')
    permissionNumberUsed = models.CharField(max_length=1, db_column='PERMISSION_NBR_USED')
    gradingBasisEnroll = models.CharField(max_length=3, db_column='GRADING_BASIS_ENRL')
    officialCourseGrade = models.CharField(max_length=3, db_column='CRSE_GRADE_OFF')

    class Meta:
        managed = False
        db_table = 'ENROLL_VW'

    def __unicode__(self):
        return "{0} {1}{2}.{3}   {4} {5},{6}".format(
            self.strm,
            self.subject,
            self.catalogNumber,
            self.classSection,
            self.username,
            self.last_name,
            self.first_name
        )

class SectionStudentManager(models.Manager):

    def sync(self):

        parents = SectionStudentParent.objects.all()

        for parent in parents:
            print parent.strm, parent.subject, parent.catalogNumber, parent.classSection, \
                parent.username, parent.first_name, parent.last_name, parent.enrolledStatus
            try:
                sectionStudent = self.get(
                    section__session__term__number=parent.strm.strip(),
                    section__classNumber=parent.classNumber.strip(),
                    student__username=parent.emplid.strip(),
                    #status=parent.status
                )
            except:
                term, new = Term.objects.get_or_create(number=parent.strm.strip())
                course, new = Course.objects.get_or_create(
                    subject__name=parent.subject.strip(),
                    number=parent.catalogNumber.strip(),
                )
                session, new = Session.objects.get_or_create(
                    term=term, course=course
                )
                section, new = Section.objects.get_or_create(
                    session=session, number=parent.classSection
                )
                student, newStudent, oldPerson = Student.objects.get_or_create_with_person(
                    username=parent.username.strip(),
                    first_name=parent.first_name.strip(),
                    last_name=parent.last_name.strip(),
                    email=parent.email.strip(),
                    level=parent.classLevel.strip()
                )
                sectionStudent, new = self.get_or_create(
                    section=section, student=student
                )
            # Reset student info in case it changes (except for SFSU ID)
            sectionStudent.student.first_name = parent.first_name.strip()
            sectionStudent.student.last_name = parent.last_name.strip()
            sectionStudent.student.email = parent.email.strip()
            sectionStudent.student.level = parent.classLevel.strip()
            #degreeProgram = DegreeProgram.objects.get(name=parent.academicPlan)
            #student.degreeProgram.add(degreeProgram)
            sectionStudent.student.save()
            sectionStudent.status = parent.enrolledStatus.strip()
            # if re.search('\d+', parent.permissionNumberUsed):
            #     sectionStudent.permissionNumber = parent.permissionNumberUsed
            # else:
            #     sectionStudent.permissionNumber = None
            if parent.officialCourseGrade:
                grade = Grade(parent.officialCourseGrade.strip())
                if sectionStudent.grade != grade:
                    sectionStudent.grade = grade
                    studentGrade, new = StudentGrade.objects.get_or_create(
                        course=sectionStudent.section.session.course,
                        student=sectionStudent.student
                    )
                    studentGrade.grade = sectionStudent.grade
                    studentGrade.save()
            sectionStudent.save()

class SectionStudent(models.Model):
    section = models.ForeignKey(Section)
    student = models.ForeignKey(Student)
    status = models.CharField(max_length=32, choices=(
        ('ENROLLED', 'Enrolled'),
        ('WAITLIST', 'Waitlisted'),
        ('UNREGISTERED', 'Unregistered'),
        ('DROPPED', 'Dropped'),
    ))
    permissionNumber = models.BigIntegerField(blank=True, null=True)
    entryDate = models.DateField(auto_now_add=True)
    updateDate = models.DateField(auto_now=True)
    passedPrerequisites = models.NullBooleanField(default=None)
    passedExams = models.NullBooleanField(default=None)
    qualified = models.NullBooleanField(default=None)
    grade = GradeField(blank=True)
    objects = SectionStudentManager()

    def checkPrerequisites(self):
        #for course in section.session.course.prerequisites.all():
        print "Checking prerequisites ..."

    def checkExams(self):
        print "Checking exams ..."

    def __unicode__(self):
        return "{0}   {1}".format(self.student.__unicode__(), self.section.__unicode__())


class Reason(models.Model):
    name=models.CharField(max_length=64, unique=True)
    description=models.CharField(max_length=512, blank=True)

    def __unicode__(self):
        return self.name


class WithdrawalReason(models.Model):
    reason = models.ForeignKey(Reason, on_delete=models.CASCADE)
    withdrawalPreferences = models.ForeignKey('WithdrawalPreferences', on_delete=models.CASCADE)
    rank = models.SmallIntegerField()

    def __unicode__(self):
        return "Withdrawal Reason {0} ({1}) for {2} ".format(self.rank,
                                                 self.reason.__unicode__(),
                                                 self.withdrawalPreferences.__unicode__()
                                                 )

class ApproverList(models.Model):
    level = models.SmallIntegerField()
    groups = models.ManyToManyField(Group)

    def __unicode__(self):
        return "Level {0} approval roles: {1}".format(self.level, self.groups.all())


class WithdrawalPreferences(models.Model):
    college = models.OneToOneField(College)
    approverLists = models.ManyToManyField(ApproverList, related_name='withdrawal_approver_for')
    denierLists = models.ManyToManyField(ApproverList, related_name='withdrawal_denier_for')
    reasons = models.ManyToManyField(Reason, through='WithdrawalReason')

    def __unicode__(self):
        return "Withdrawal preferences for {0}".format(self.college.__unicode__())


class Withdrawal(models.Model):
    sectionStudent = models.OneToOneField(SectionStudent)
    approvedBy = models.ManyToManyField(Person, blank=True,
                                        related_name='approved_withdrawals')
    deniedBy = models.ManyToManyField(Person, blank=True,
                                      related_name='denied_withdrawals')
    approvalLevel = models.SmallIntegerField(default=0)
    status = models.NullBooleanField(default=None, choices=((True,'APPROVED'),
                                                            (None,'WAITING'),
                                                            (False,'DENIED'),
                                                            ))
    def __unicode__(self):
        return "Withdrawal for {0}".format(self.sectionStudent.__unicode__())

    def college(self):
        acadOrg = self.sectionStudent.section.session.course.subject.host
        try:
            return acadOrg.department.college
        except:
            print "{0} is not a department".format(acadOrg.__unicode__())
        try:
            return acadOrg.school.college
        except:
            print "{0} is not a school".format(acadOrg.__unicode__())
        return None

    def approve(self, person):
        self.approvedBy.add(person)
        return self.update()

    def deny(self, person):
        self.deniedBy.add(person)
        return self.update()

    def update(self):
        """
        returns current approval level:
        L=0     no approvals or denials yet (status set to WAITING)
        L<0     denied at level |L| (status set to DENIED if |L|=Lmax, WAITING otherwise)
        L>0     approved at level L (status set to APPROVED if L=Lmax, WAITING otherwise)
        """
        try:
            preferences = WithdrawalPreferences.objects.get(college=self.college())
        except:
            print 'Problem retrieving withdrawal preferences'
            return None
        approvedByRoles = set()
        for person in self.approvedBy.all():
            for role in person.groups.all():
                approvedByRoles.add(role)
        approverLists = preferences.approverLists.order_by('-level')
        if approverLists is None:
            print 'Problem with approverLists'
            return None
        maxApprovalLevel = approverLists[0].level
        for approverList in approverLists:
                if approverList.level > abs(self.approvalLevel):
                    if len(approvedByRoles.intersection(set(approverList.groups.all())))!=0:
                        self.approvalLevel = approverList.level
        if self.approvalLevel == maxApprovalLevel:
                    self.status = True
        deniedByRoles = set()
        for person in self.deniedBy.all():
            for role in person.groups.all():
                deniedByRoles.add(role)
        denierLists = preferences.denierLists.order_by('level')
        if denierLists is None:
            print 'Problem with denierLists'
            return None
        minDenialLevel = -denierLists[0].level
        for denierList in denierLists:
            if denierList.level > abs(self.approvalLevel):
                if len(deniedByRoles.intersection(set(denierList.groups.all()))) != 0:
                    self.approvalLevel = -approverList.level
        if self.approvalLevel == minDenialLevel:
            self.status = False
        self.save()
        return self.status










# class SectionStudentNote(models.Model):
#     sectionStudent = models.ForeignKey(SectionStudent)
#     note = models.TextField()
#     entryDate = models.DateField(auto_now_add=True)


# class Exam(models.Model):
#     name = models.CharField(max_length=32)
#     description = models.CharField(max_length=128)
#     zeusType = models.CharField(max_length=5)
#     policyDate = models.DateField()
#     minPassScore = models.IntegerField()
#     maxFailScore = models.IntegerField(blank=True, null=True)
#     validDays = models.IntegerField(blank=True, null=True)
#
#     def __unicode__(self):
#         return self.name


# class ExamScoreManager(Importer):
#     selections = 'STU_ID, TEST_DATE, TEST_SCORE'
#     table = 'SIMSR.SF_TOS_ZEUS'
#     conditions = ''
#
#     def conditionsSQL(self, exam, term):
#
#         firstDate = term.startDate - datetime.timedelta(
#             days=exam.validDays)
#         lastDate = term.startDate + datetime.timedelta(
#             weeks=816)
#         conditionList = []
#         self.params = []
#         conditionList.append('TEST_TYPE LIKE %s')
#         self.params.append(exam.zeusType)
#         conditionList.append("TEST_DATE >= %s")
#         self.params.append(firstDate)
#         conditionList.append("TEST_DATE <= %s")
#         self.params.append(lastDate)
#         self.conditions = ' AND '.join(conditionList)
#
#     def importExternal(self, exam, term):
#         self.conditionsSQL(exam, term)
#         self.sql = 'SELECT {0} FROM {1} WHERE {2}'.format(
#             self.selections,
#             self.table,
#             self.conditions)
#         print self.sql
#         print self.params
#         for uid, test_datetime, test_score in self.lookup():
#             test_date = test_datetime.date()
#             print uid, test_date, test_score
#             try:
#                 student = Student.objects.get(uid=uid.strip())
#             except:
#                 continue
#             examScore = self.get_or_create(
#                 student=student,
#                 date=test_date, exam=exam,
#                 score=test_score
#             )


# class ExamScore(models.Model):
#     exam = models.ForeignKey(Exam)
#     date = models.DateField()
#     student = models.ForeignKey(Student)
#     score = models.IntegerField()
# #    objects = ExamScoreManager()
#
#     def success(self, term):
#         if self.exam.validDays is not None:
#             if (term.startDate - self.date).days > self.exam.validDays:
#                 return False
#         if self.score >= self.exam.minPassScore: return True
#         if self.score <= self.exam.maxFailScore: return False
#         return None
#
#     def __unicode__(self):
#         return "{0}   {1}".format(self.student.__unicode__(),
#                                   self.exam.__unicode__()
#         )




# class DegreeCourse(models.Model):
#     degree = models.ForeignKey('DegreeProgram',
#                                 related_name='degree_courses'
#     )
#     course = models.ForeignKey(Course,
#                                 related_name='course_degrees'
#     )
#     gradeList = sorted(list(Grade(i) for i in Grade.validGrades.keys()),
#                        reverse=True)
#     choices = tuple(tuple([i, i]) for i in gradeList)
#     passingGrade = GradeField(choices=choices)
#
#     def __unicode__(self):
#         return self.degree.name + ' requires ' + \
#                self.passingGrade.letterGrade + ' or better in ' + \
#                self.course.name
#
#     def passed(self, student):
#         studentGrades = StudentGrade.objects.filter(
#             course=self.course, student=student
#         )
#         if studentGrades:
#             for studentGrade in studentGrades:
#                 if studentGrade.grade >= self.passingGrade:
#                     return True
#         return False
#



# class DegreeCourseGroup(models.Model):
#     degreeCourses = models.ManyToManyField(DegreeCourse)
#     units = models.SmallIntegerField()
#
#     def passed(self, student):
#         count = 0
#         for degreeCourse in self.degreeCourses.all():
#             if degreeCourse.passed(student):
#                 count += degreeCourse.course.units()
#                 if count >= self.units:
#                     return True
#         return False


#class DegreeCourseGroup(models.Model):
     



class DegreeStudentParent(models.Model):

    id = models.CharField(max_length=21, db_column='ID', primary_key=True)
    emplid = models.CharField(max_length=11, db_column='EMPLID')
    academicCareer = models.CharField(max_length=4, db_column='acad_career')
    studentCareerNumber = models.IntegerField(db_column='STDNT_CAR_NBR')
    effectiveDate = models.DateTimeField(db_column='EFFDT')
    effectiveSequence = models.IntegerField(db_column='EFFSEQ')
    academicPlan = models.CharField(max_length=10, db_column='ACAD_PLAN')
    declareDate = models.DateTimeField(db_column='DECLARE_DT')
    planSequenceNumber = models.IntegerField(db_column='PLAN_SEQUENCE')
    reqTerm = models.CharField(max_length=4, db_column='REQ_TERM')
    completionTerm = models.CharField(max_length=4, db_column='COMPLETION_TERM')
    studentDegreeNumber = models.CharField(max_length=2, db_column='STDNT_DEGR')
    degreeCheckoutStatus = models.CharField(max_length=2, db_column='DEGR_CHKOUT_STAT')

    class Meta:
        managed = False
        db_table = 'DEGREE_STUDENT'


#class DegreeStudent(models.Model):


class DegreeParent(models.Model):
    academicPlan = models.CharField(max_length=10, db_column='ACAD_PLAN', primary_key=True)
    academicOrganization = models.CharField(max_length=10, db_column='ACAD_ORG')
    dateCreated = models.DateTimeField(blank=True, null=True, db_column='DATE_CREATED')
    dateModified = models.DateTimeField(blank=True, null=True, db_column='LAST_MODIFIED')

    class Meta:
        managed = False
        db_table = 'DEGREE'

    def __unicode__(self):
        return self.academicPlan


class DegreeManager(models.Manager):

    def sync(self):
        for parent in DegreeParent.objects.all():
            degree, new = self.get_or_create(academicPlan=parent.academicPlan)
            if new:
                acadOrg, new = AcademicOrganization.objects.get_or_create(
                    databaseColumnName = parent.academicOrganization
                )
                degree.name = 'Degree'
                degree.academicOrganization = acadOrg
                degree.dateCreated = parent.dateCreated
                degree.dateModified = parent.dateModified


class Degree(models.Model):

    name = models.CharField(blank=True, null=True, max_length=128)
    academicPlan = models.CharField(max_length=10, unique=True, primary_key=True)
    academicOrganization = models.ForeignKey(AcademicOrganization, null=True)
    dateCreated = models.DateTimeField(null=True)
    dateModified = models.DateTimeField(null=True)
    objects = DegreeManager()
    #requiredCourses = models.ManyToManyField(Course, blank=True)

    def __unicode__(self):
        return "{0} {1}".format(self.name, self.academicOrganization)


class DegreeStudent(models.Model):
    student = models.ForeignKey(Student)
    degree = models.ForeignKey(Degree)


# class AleksClass(models.Model):
#
#     site = 'https://www.aleks.com'
#     classKey = models.CharField(max_length=255, unique=True)
#     className = models.CharField(max_length=128)
#     classTerm = models.ForeignKey(Term)
#
#     def __unicode__(self):
#         return self.classKey
#
# class AleksStudentManager(models.Manager):
#
#     def update(self):
#
#         aleksClasses = aleksClass.objects.get(
#             term__startDate__gte=datetime.date.today()
#         )
#         driver = webdriver.PhantomJS(service_args=
#                              ['--ignore-ssl-errors=true',
#                               '--ssl-protocol=any'])
#         driver.wait = WebDriverWait(driver, 20)
#         driver.get(self.site)
#
#         # login
#         username = driver.wait.until(EC.presence_of_element_located(
#             (By.ID, "username")))
#         username.clear()
#         username.send_keys("mgolterman")
#         password = driver.wait.until(EC.presence_of_element_located(
#             (By.ID, "password")))
#         password.clear()
#         password.send_keys("thisisnew")
#         login = driver.wait.until(EC.element_to_be_clickable(
#             (By.ID,"login")))
#         login.submit()
#
#         # go to class page
#
#         for aleksClass in aleksClasses:
#             driver.wait.until(EC.presence_of_element_located(
#                 (By.ID,'sim_search_val'))).send_keys(
#                 aleksClass.class_key)
#             driver.wait.until(EC.presence_of_element_located(
#                 (By.ID,'sim_search_go'))).click()
#             linkEntry = driver.wait.until(EC.presence_of_element_located(
#                 (By.CLASS_NAME, 'td_2')))
#             link = linkEntry.find_element_by_tag_name('a').click()
#
#             tile = driver.wait.until(EC.presence_of_all_elements_located(
#                 (By.ID, 'overall_tile')))
#             spans = tile[0].find_elements_by_tag_name('span')
#             ndspans = numpy.array([spans[i].get_attribute('innerHTML')[0:8]
#                                     for i in range(len(spans))])
#             spans[(ndspans == 'View All').nonzero()[0]].click()
#
#             # get student data from 12th table in progress_report_class div
#
#             report = driver.find_element_by_id('progress_report_class')
#             tables = report.find_elements_by_tag_name('table')
#             rows = tables[11].find_elements_by_tag_name('tr')
#             nHeaderRows = 13
#             nStudents = (len(rows) - nHeaderRows)/2
#             print 'nStudents = ', nStudents
#             aleksStudents = []
#             for i in range(nStudents):
#                 aleksStudent = {}
#                 aleksStudent['EMPLID'] = None
#                 j = i*2 + nHeaderRows + 1
#                 studentData = rows[j].text.split('\n')
#                 #print studentData
#                 if re.search('No Knowledge', rows[j].text):
#                     studentProgress = 0.
#                 else:
#                     studentProgress = sum(numpy.array(
#                         (studentData[7][:-1].split(
#                             ' +'))).astype('float'))
#                 name = studentData[0].split(',')
#                 aleksStudent['FIRST_NAME'] = name[1]
#                 aleksStudent['LAST_NAME'] = name[0]
#                 aleksStudent['PROGRESS'] = studentProgress
#                 aleksStudents.append(aleksStudent)
#                 print name[1], name[0], studentProgress
#             idColumn = tables[13].find_elements_by_tag_name('td')[1]
#             idColumn.click()
#             rows = tables[11].find_elements_by_tag_name('tr')
#             for i in range(nStudents):
#                 j = i*2 + nHeaderRows + 1
#                 studentData = rows[j].text.split('\n')
#                 #print studentData
#                 if re.search('^\d{9}$', studentData[0]):
#                     aleksStudents[i]['EMPLID'] = studentData[0]
#                 print aleksStudents[i]['FIRST_NAME'], aleksStudents[i]['LAST_NAME'],aleksStudents[i]['EMPLID'], aleksStudents[i]['PROGRESS']
#                 aleksStudent, new = self.get_or_create(
#                     emplid=aleksStudents[i]['EMPLID'],
#                     firstName = aleksStudents[i]['FIRST_NAME'],
#                     lastName = aleksStudents[i]['LAST_NAME'],
#                     progress = aleksStudents[i]['PROGRESS']
#                 )
#
#         driver.quit()
#
# class AleksStudent(models.Model):
#
#     emplid = models.CharField(max_length=9)
#     firstName = models.CharField(max_length=64)
#     lastName = models.CharField(max_length=64)
#     progress = models.FloatField(blank=True, null=True)
#
#     objects = AleksStudentManager()
#
#     def __unicode__(self):
#         return "{0}  {1} {2}:   {3}".format(self.emplid,
#                                             self.firstName,
#                                             self.lastName,
#                                             self.progress)

class TermInstructorManager(models.Manager):

    def propagateInstructorsToTerm(self, termNumber=''):
        try:
            term = Term.objects.get(number=termNumber)
        except:
            return False
        for termInstructor in self.all():
            instructor = termInstructor.instructor
            propagated, new = self.get_or_create(instructor=instructor, term=term)
            if new:
                print propagated
        return True



class TermInstructor(models.Model):

    term = models.ForeignKey(Term)
    instructor = models.ForeignKey(Person)
    requestedLoad = models.IntegerField(blank=True, null=True)
    approvedLoad = models.IntegerField(blank=True, null=True)
    objects = TermInstructorManager()

    def __unicode__(self):
        return '{0}  {1} {2}'.format(self.term.number, self.instructor.first_name,
                                 self.instructor.last_name
        )

class SectionPreferenceManager(models.Manager):

    def createFromConflicts(self, instructors=None, sections=None):
        if instructors==None or sections==None:
            return
        for section in sections:
            msg = section.__unicode__() + ':    '
            for instructor in instructors:
                person = instructor.person_ptr
                sectionPreference, new = self.get_or_create(
                    section=section, instructor=person,
                )
                if person.conflictsWith(section):
                    sectionPreference.preference=0
                else:
                    sectionPreference.preference=1
                    msg += instructor.last_name + ', '
                sectionPreference.save()
            print msg

    def countInstructorsForSection(self, section):
        return SectionPreference.objects.filter(
            section=section, preference__gte=1,
        ).count()

    def getLDLabSectionsWithNoPossibleInstructors(self, termNumber=''):
        for section in Section.objects.getLDLabSections(termNumber=termNumber):
            print section
            if self.countInstructorsForSection(section) == 0:
                print section, ' has no possible instructors'


    def getPreferences(self, excelFile, only=''):
        gtaGroup = Group.objects.get(name='GTA')
        sheet = pd.read_excel(excelFile, header=0)
        term = Term.objects.get(number='2183')
        ldLabSections = Section.objects.filter(
            session__term=term,
            session__course__number__lt=300,
            courseType__name='LAB'
        ).exclude(
            number__contains='Z'
        ).order_by(
            'session__course__subject__name',
            'session__course__number','number'
        )
        nLDLabSections = ldLabSections.count()
        print nLDLabSections, 'lower division labs'
        gtaSections = Section.objects.filter(
            session__course__number__gte=300
        ).exclude(
            courseType__name='SUP'
        ).exclude(
            number__contains='Z'
        ).order_by(
            'session__course__subject__name',
            'session__course__number', 'number'
        )
        nGTASections = gtaSections.count()
        #conflicts = numpy.zeros(shape = (nGTASections, nLDLabSections), dtype=numpy.int)
        print nGTASections, 'GTA courses'
        #return
        for i in range(31):             # instructors
            firstName = sheet['First Name'][i]
            lastName = sheet['Last Name'][i]
            emplid = unicode(int(sheet['SFSU ID'][i]))
            email = sheet['Email'][i]
            instructorType = sheet['GTA/LEC'][i]
            #instructorPriority = int(sheet['PRIORITY'][i])
            if only != '':
                if only != instructorType:
                    continue
            requestedLoad = sheet['Desired Load'][i]
            approvedLoad = sheet['Approved Load'][i]
            gta = instructorType == 'GTA'
            instructor, new = Person.objects.get_or_create(
                username=emplid
            )
            #instructor.gta = gta
            if gta:
                instructor.groups.add(gtaGroup)
            #instructor.priority = instructorPriority
            if new:
                instructor.first_name = firstName
                instructor.last_name = lastName
                instructor.email = email
                #instructor.instructorType = instructorType
            instructor.save()
            print instructor
            termInstructor, new = TermInstructor.objects.get_or_create(
                term=term, instructor=instructor
            )
            termInstructor.requestedLoad = requestedLoad
            termInstructor.approvedLoad = approvedLoad
            termInstructor.save()
            #term.instructors.add(instructor)
            for j in range(61):         # sections to assign
                sectionName = sheet.columns[j+8]
                #print sectionName
                section = ldLabSections.filter(
                    session__course__subject__name=sectionName[0:4],
                    session__course__number=sectionName[5:8],
                    number=sectionName[9:11]
                )
                section = section[0]
                #print section
                preference = int(sheet.iloc[i][j+8])
                try:
                    sectionPreference = SectionPreference.objects.get(
                        section=section, instructor=instructor
                    )
                    sectionPreference.preference = preference
                except:
                    sectionPreference = SectionPreference.objects.create(
                        section=section, instructor=instructor, preference=preference
                    )
                # if preference != 0 and gtaGroup in instructor.groups.all():
                #     for k in range(14):     # GTA's own class plans
                #         attending = sheet.iloc[i][k+69]
                #         gtaCourseName = sheet.columns[k+69]
                #         #if k==14:
                #         #print gtaCourseName
                #         theseSections = gtaSections.filter(
                #             session__course__subject__name=gtaCourseName[0:4],
                #             session__course__number=gtaCourseName[5:8]
                #         )
                #         #print theseSections
                #         if attending == 'Yes' or attending == 'Maybe':
                #             for thisSection in theseSections:
                #                 #print section, gtaSection, ' checking for conflict'
                #                 if section.conflicts.filter(pk=thisSection.pk).exists():
                #                     print section, thisSection, 'conflict: setting section preference to 0'
                #                     sectionPreference.preference = 0
                sectionPreference.save()

    def zimpl(self, file='/Users/marzke/Department/Spring2018/input.zpl',
              termNumber='2183'):

        out = open(file, 'w')

        # write instructors
        sectionPreferences = SectionPreference.objects.filter(
            section__session__term__number='2183'
        ).order_by(
            'instructor__last_name', 'instructor__first_name',

        ).distinct(
            'instructor__last_name', 'instructor__first_name'
        )

        #instructors = sectionPreferences.values_list('instructor__last_name')
        instructorString = 'set I :={'
        for sectionPreference in sectionPreferences:
            instructorString += '"%s",' % re.sub('\s', '_', sectionPreference.instructor.last_name)
        instructorString = instructorString[:-1] + '};\n'
        out.write(instructorString)

        # write sections
        #sections = Section.objects.getLDLabSections(termNumber=termNumber)
        DsectionPreferences = SectionPreference.objects.filter(
            section__session__term__number='2183'
        ).distinct(
            'section__session__course__subject__name',
            'section__session__course__number',
            'section__number'
        ).order_by(
            'section__session__course__subject__name',
            'section__session__course__number',
            'section__number'
        )
        sections = []
        sectionString = 'set S :={'
        for DsectionPreference in DsectionPreferences:
            section = DsectionPreference.section
            sections.append(section)
            sectionString += '"%s",' % section.__unicode__()
        sectionString = sectionString[:-1] + '}'
        out.write(sectionString + ";\n")

        # write preferences
        pString = 'param P[I*S] := '
        pString += '| %s |' % sectionString[9:-1]
        out.write(pString + "\n")
        pString = ''
        for sectionPreference in sectionPreferences:
            print sectionPreference
            pString += ' | "%s" |' % re.sub('\s', '_', sectionPreference.instructor.last_name)
            for section in sections:
                print section
                otherSectionPreference = SectionPreference.objects.get(
                    section=section, instructor=sectionPreference.instructor
                )
                pString += ' %s,' % otherSectionPreference.preference
            pString = pString[:-1] + " |\n"
        out.write(pString[:-1] + ';\n')

        # write approved max loads
        pString = 'param L[I] :='
        for sectionPreference in sectionPreferences:
            termInstructor = TermInstructor.objects.get(
                term=sectionPreference.section.session.term,
                instructor=sectionPreference.instructor
            )
            pString += ' <"%s"> ' % re.sub('\s', '_', sectionPreference.instructor.last_name)
            pString += '%s,' % termInstructor.approvedLoad
        pString = pString[:-1] + ';\n'
        out.write(pString)

        # write out sameCourse matrix
        # pString = 'param C[I*I] := '
        # pString += '| %s |' % sectionString[9:-1]
        # pString += "\n"
        # for section1 in sections:
        #     course1 = section1.session.course_id
        #     name1 = ' | "%s" |' % section1.__unicode__()
        #     pString += name1
        #     for section2 in sections:
        #         sameCourse = '0'
        #         course2 = section2.session.course_id
        #         if course1 == course2:
        #             sameCourse = '1'
        #         pString += ' %s,' % sameCourse
        #     pString = pString[:-1] + '|\n'
        # pString = pString[:-1] + ';\n'
        # out.write(pString)

        # write variables
        out.write('var x[I*S] binary;\n')

        # write what to optimize: total preference + same class
        out.write('maximize score: sum <i,s> in I*S: P[i,s] * x[i, s];\n')
                 # + sum <j,k> in S*S: C[j,k] * x[j,k];\n')


        # write overall constraints
        out.write('subto oneInstructorPerSection: forall <s> in S do sum <i> in I: x[i,s] == 1;\n')
        out.write('subto noZeroPreferences: forall <i,s> in I*S do P[i,s] - x[i,s] >= 0;\n')

        # write per-instructor section time conflict constraints
        nConstraints = 2
        for sectionPreference in sectionPreferences:
            instructor = sectionPreference.instructor
            lastName = re.sub('\s', '_', sectionPreference.instructor.last_name)
            print lastName
            if True: #instructor.priority == 2:
                iString = 'subto load_%s: forall <i> in {"%s"} do sum <s> in S: x[i,s] == L[i];\n' % (lastName, lastName)
            else:
                iString = 'subto load%s: forall <i> in {"%s"} do sum <s> in S: x[i,s] <= L[i];\n' % (lastName, lastName)
            out.write(iString)
            for i in range(len(sections)):
                section1 = sections[i]
                sectionPreference1 = SectionPreference.objects.get(
                    section=section1, instructor=instructor
                )
                for j in range(i+1, len(sections)):
                    section2 = sections[j]
                    sectionPreference2 = SectionPreference.objects.get(
                        section=section2, instructor=instructor
                    )
                    if sectionPreference1.preference > 0 and sectionPreference2.preference > 0:
                        if section1.conflictsWith(section2):
                            nConstraints += 1
                            cString = 'subto conflict%s' % lastName
                            cString += str(i).strip()
                            cString += str(j).strip()
                            cString += ': forall <i> in {"%s"} do sum <s> in ' % lastName
                            cString += '{"%s", ' % section1.__unicode__()
                            cString += '"%s"}: x[i,s] <= 1;\n' % section2.__unicode__()
                            out.write(cString)
        print nConstraints
        #forall < s > in S do sum < i > in I: x[i, s] == 1;
        # forall <i,s> where x[i,s]==1: obj[i,s] >= 1;
        out.close()



class SectionPreference(models.Model):

    section = models.ForeignKey(Section)
    instructor = models.ForeignKey('Person')
    preference = models.IntegerField(default=0,
        verbose_name='Section Preference',
        choices=(
        (0, 'Impossible'),
        (1, 'Possible'),
        (2, 'Preferred'),
        (3, 'Best'),
    ))
    objects = SectionPreferenceManager()

    class Meta:
        unique_together = (('section','instructor'),)

    def __unicode__(self):
        return '{0} {1}   {2}'.format(self.section.__unicode__(), self.instructor.__unicode__(), unicode(self.preference))

    def get_absolute_url(self):
        return "/PA/SectionPreference/%i/" % self.id
        # from django.urls import reverse
        # return reverse('people.views.details', args=[str(self.id)])

# class Position(models.Model):
#
#     employees = models.ManyToManyField(Person, through='Appointment')
#     departmentCode = models.CharField(max_length=4)
#     positionCode = models.CharField(max_length=2)


# class Appointment(models.Model):
#
#     person = models.ForeignKey(Person)
#     position = models.ForeignKey(Position)
#     termChoices = (
#         ('Semester','Semester'),
#         ('OneYear', 'OneYear'),
#         ('ThreeYear', 'ThreeYear'),
#     )
#     term = models.SmallIntegerField(choices=termChoices)
#     timeBase = models.DecimalField(decimal_places=2, max_digits=8)
#     monthlyBaseSalary = models.DecimalField(decimal_places=2, max_digits=8)
#     fullTimeWTU = 15.0
#     monthsPerSemester = 6
#
#     def __unicode__(self):
#         return '{0} {1} {2} {3}'.format(self.person.__unicode__(), self.position.__unicode__(),
#                                     self.term, self.timeBase)
#
#     def monthlySalary(self):
#         return self.monthlyBaseSalary * timeBase
#
#     def semesterSalaryForWTU(self, wtu):
#         return self.monthlyBaseSalary * self.timeBaseForWTU(wtu)
#
#     def semesterSalary(self):
#         return self.monthlySalary() * self.monthsPerSemester
#
#     def timeBaseForWTU(self, wtu):
#         return round(wtu / self.fullTimeWTU)


class LeaveManager(models.Manager):

    def importFromExcel(self, file):
        typeDict = {'Leave':'LWOP', 'Leave W/Py':'LWDIP', 'Sabbatical':'Sabbatical'}
        df = pd.read_excel(file, header=1, na_values=['NA'])
        for i in range(len(df['ID'])):
            person, new = Person.objects.get_or_create(username=df['ID'].iloc[i])
            if new:
                person.last_name = df['Last'].iloc[i]
                person.first_name = df['First Name'].iloc[i]
            effectiveDate = df['Eff Date'].iloc[i]
            returnDate = df['Return Dt'].iloc[i]
            type = typeDict[df['Pay Status'].iloc[i]]
            FTE = df['FTE'].iloc[i]
            leave, new = self.get_or_create(
                person=person, effectiveDate=effectiveDate, returnDate=returnDate,
                type=type, FTE=FTE,
            )
            leave.save()


class Leave(models.Model):
    person = models.ForeignKey(Person)
    effectiveDate = models.DateField(blank=True, null=True)
    returnDate = models.DateField(blank=True, null=True)
    type = models.CharField(max_length=60,
                            choices=(
        ('Sabbatical', 'Sabbatical'),
        ('LWDIP', 'Leave With Difference in Pay'),
        ('LWOP', 'Leave Without Pay'),
    ))
    FTE = models.FloatField(blank=True, null=True)
    objects = LeaveManager()

    def __unicode__(self):
        return '{0}: {1} {2}'.format(self.person.username,
                                     self.person.first_name,
                                     self.person.last_name)


class FERPManager(models.Manager):

    def importFromExcel(self, file):
        df = pd.read_excel(file, header=1, na_values=['NA'])
        for i in range(len(df['UIN'])):
            person, new = Person.objects.get_or_create(username=df['UIN'].iloc[i])
            if new:
                person.last_name = df['Last'].iloc[i]
                person.first_name = df['First Name'].iloc[i]
            startDate = df['Appt End Date'].iloc[i]
            endDate = df['FERP Elig End'].iloc[i]
            FTE = df['FTE'].iloc[i]
            FERP, new = self.get_or_create(
                person=person, startDate=startDate, endDate=endDate,
                FTE=FTE,
            )
            FERP.save()


class FERP(models.Model):
    person = models.ForeignKey(Person)
    startDate = models.DateField(blank=True, null=True)
    endDate = models.DateField(blank=True, null=True)
    FTE = models.FloatField(blank=True, null=True)
    objects = FERPManager()

    def __unicode__(self):
        return '{0}: {1} {2}'.format(self.person.username,
                                     self.person.first_name,
                                     self.person.last_name)


class CommitteeManager(models.Manager):

    def importFromExcel(self):
        df = pd.read_excel(file, header=0, na_values=['NA'])
        for i in range(len(df['ACAD_GROUP'])):
            acadGroup = df['ACAD_GROUP'].iloc[i]
            acadOrg = df['ACAD_ORG'].iloc[i]
            name = df['NAME'].iloc[i]
            nickname = df['NICKNAME'].iloc[i]
            description = df['DESCRIPTION'].iloc[i]
            committee, new = self.get_or_create(
                acadGroup=acadGroup, acadOrg=acadOrg, name=name)
            committee.nickname = nickname
            committee.description = description
            committee.save()


class Committee(models.Model):
    members = models.ManyToManyField(Person, blank=True, through='CommitteePerson')
    acadOrg = models.ForeignKey(AcademicOrganization, blank=True, null=True)
    acadGroup = models.ForeignKey(AcademicGroup, blank=True, null=True)
    name = models.CharField(max_length=64)
    nickname = models.CharField(max_length=8, blank=True)
    description = models.CharField(max_length=512, blank=True)
    size = models.SmallIntegerField()
    termYears = models.SmallIntegerField(blank=True, null=True)
    objects = CommitteeManager()

    def __unicode__(self):
        if self.acadOrg:
            return "{0}, {1}: {2}".format(self.acadOrg, self.acadGroup, self.name)
        else:
            return "{0}: {1}".format(self.acadGroup, self.name)

    class Meta:
        unique_together = ('acadOrg', 'acadGroup', 'name')


class CommitteePersonRole(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=256, blank=True)

    def __unicode__(self):
        return self.name


class CommitteePersonManager(models.Manager):

    def addOrUpdate(self, person, committee, voting, role):
        committeePerson, new = self.get_or_create(person=person, committee=committee)
        committeePerson.voting = voting
        committeePerson.role = role
        committeePerson.save()
        return committeePerson, new


class CommitteePerson(models.Model):
    person = models.ForeignKey(Person)
    committee = models.ForeignKey(Committee)
    voting = models.BooleanField(default=False)
    role = models.ForeignKey(CommitteePersonRole, blank=True)
    termStart = models.DateField()
    termEnd = models.DateField()
    objects = CommitteePersonManager()

    def __unicode__(self):
        return "{0}---{1}".format(self.person, self.committee)

