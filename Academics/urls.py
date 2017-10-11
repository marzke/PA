from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^\d{9}$', views.LandingView.as_view()),
    url(r'sections/', views.Sections.as_view()),
    url(r'sectionPreferences/', views.sectionPreferences, name='sectionPreferences'),
    url(r'admin/', admin.site.urls),
]
