from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import *

urlpatterns = patterns('',
    url(r'^$', pagina_index),
    url(r'^registro/$',registro), 
   	url(r'^login/$',login_usuario), 
   	url(r'^perfil/$',perfil),  
   	url(r'^logout/$',logout_usuario),
   	url(r'^categoria/$',addCategoria),
   	url(r'^respuestas/$',addRespuesta),
   	url(r'^preguntas/$',addPregunta),
   	url(r'^actualizar/$',set_registro),
	url(r'^detalle_pregunta/(?P<id>\d+)$',detalle_pregunta),
	url(r'^editar_pregunta/(?P<id>\d+)$',editar_pregunta),

)