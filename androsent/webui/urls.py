from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from . import views
from django.views.generic import TemplateView
urlpatterns = [
    url(r'^$', views.index,name="index"),
    url(r'^samsung/$', views.samsung,name="samsung"),
    url(r'^samsung_show/$', views.samsung_show,name="samsung"),
    url(r'^upload/$', views.SaveProfile,name="uploads"),
    url(r'^getsentiment/$', views.handle_ip_file,name="uploads"),
       
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
