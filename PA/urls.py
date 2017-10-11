from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [url(r'^admin/', admin.site.urls),
               url(r'^$', views.index, name='index'),
               url(r'^PA/', include('Academics.urls')),]
    # Examples:
    # url(r'^$', 'PA.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


