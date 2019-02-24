from django.contrib import admin
from django.contrib.admin import ModelAdmin

from Academics.models import *

class PersonAdmin(ModelAdmin):
    ordering = ('last_name', 'first_name',)

class AcademicOrganizationAdmin(ModelAdmin):
    ordering = ('databaseColumnName',)

class CollegeAdmin(ModelAdmin):
    ordering = ('name',)

class DepartmentAdmin(ModelAdmin):
    ordering = ('name',)

class ProgramAdmin(ModelAdmin):
    ordering = ('name',)

class KFactorAdmin(ModelAdmin):
    ordering = ('CSNumber',)

class TermAdmin(ModelAdmin):
    fields = ['season', 'year']

class SubjectAdmin(ModelAdmin):
    ordering = ('name',)

class CourseAdmin(ModelAdmin):
    ordering = ('subject__name', 'number',)

class SessionAdmin(ModelAdmin):
    ordering = ('term__number', 'course__subject__name', 'course__number',)

class SectionAdmin(ModelAdmin):
    ordering = ('session__term__number', 
                'session__course__subject__name',
                'session__course__number',
                'number',
    )

class StudentAdmin(ModelAdmin):
    ordering = ('last_name','first_name',)
    list_display = ('last_name', 'first_name', 'username',)

class GTAAdmin(ModelAdmin):
    ordering = ('last_name', 'first_name',)
    list_display = ('last_name', 'first_name', 'username',)

class LecturerAdmin(ModelAdmin):
    ordering = ('last_name','first_name',)
    list_display = ('last_name', 'first_name', 'username',)

class SectionStudentAdmin(ModelAdmin):
    ordering = ('student__last_name',
                'student__first_name',
    )

class WithdrawalAdmin(ModelAdmin):
    fields = ('sectionStudent', 'approvalLevel','status',)

# class ExamScoreAdmin(ModelAdmin):
#     ordering = ('student__last_ame','student__first_name',
#                 'date', 'score'
#     )
#     list_display = ('student','score','date',
#     )
#
# class DegreeProgramAdmin(ModelAdmin):
#     ordering = ('name',)
admin.site.register(WeeklyEvent)
admin.site.register(Person, PersonAdmin)
#admin.site.register(Professor)
admin.site.register(Student, StudentAdmin)
admin.site.register(Lecturer, LecturerAdmin)
admin.site.register(GTA, GTAAdmin)
admin.site.register(AcademicOrganization)
admin.site.register(AcademicGroup)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Program, ProgramAdmin)
#admin.site.register(University)
#admin.site.register(Campus)
admin.site.register(College, CollegeAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(KFactor, KFactorAdmin)
admin.site.register(Term, TermAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(SectionStudent, SectionStudentAdmin)
admin.site.register(CourseType)
# admin.site.register(Exam)
# admin.site.register(ExamScore, ExamScoreAdmin)
admin.site.register(Prerequisite)
admin.site.register(SessionCorrelation)
admin.site.register(SessionConflict)
admin.site.register(StudentGrade)
admin.site.register(SectionPreference)
admin.site.register(TermInstructor)
#admin.site.register(DegreeCourse)
#admin.site.register(DegreeCourseGroup)
admin.site.register(Degree)
admin.site.register(ApproverList)
admin.site.register(WithdrawalPreferences)
admin.site.register(Withdrawal)
admin.site.register(Reason)
admin.site.register(WithdrawalReason)