from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url(r'^$', views.index, name='index'),
    url(r'sections/', views.index, name='test'), #views.Sections.as_view()),
    url(r'^\d{9}$', views.LandingView.as_view()),
#    url(r'SectionPreference/(?P<pk>[0-9]+)/$', views.SectionPreferenceView.as_view(), name='sectionpreference-update'),
    url(r'SectionPreference/(?P<pk>[0-9]+)/$', views.SectionPreferenceFunctionView, name='sectionpreference-update'),
    url(r'SectionPreferences/(?P<termNumber>[0-9]+)/$', views.SectionPreferencesView, name='sectionpreferences-update'),
    url(r'admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
