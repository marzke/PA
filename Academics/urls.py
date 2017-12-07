from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'sections/', views.index, name='test'), #views.Sections.as_view()),
    url(r'^\d{9}$', views.LandingView.as_view()),
#    url(r'SectionPreference/(?P<pk>[0-9]+)/$', views.SectionPreferenceView.as_view(), name='sectionpreference-update'),
    url(r'SectionPreference/(?P<pk>[0-9]+)/$', views.SectionPreferenceFunctionView, name='sectionpreference-update'),
    url(r'SectionPreferences/(?P<termNumber>[0-9]+)/$', views.SectionPreferencesView, name='sectionpreferences-update'),
    url(r'admin/', admin.site.urls),
]
