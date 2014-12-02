from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import *

urlpatterns = patterns('',
	url(r'^permit/$', error_permisos),
	url(r'^error_eliminarpregunta/$', error_eliminarpregunta),
	url(r'^error_modificarpregunta/$', error_modificarpregunta),
	url(r'^error_eliminarrespuesta/$', error_eliminarrespuesta),
	url(r'^error_modificarrespuesta/$', error_modificarrespuesta),
)