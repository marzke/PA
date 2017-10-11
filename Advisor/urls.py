from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views


urlpatterns = patterns('',
    url(r'^start', views.start),
    url(r'^courses', views.courses_json),
    url(r'^grades', views.student_grades_json),
)
