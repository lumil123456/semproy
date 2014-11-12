from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import *

urlpatterns = patterns('',
  url(r'^$', pagina_index),
  url(r'^registro/$',registro), 
  url(r'^login/$',login_usuario), 
  url(r'^perfil/$',perfil),  
  url(r'^perfil/agregar/$',perfil_agregar),  
  url(r'^logout/$',logout_usuario),
  url(r'^categoria/$',addCategoria),
  url(r'^respuestas/$',addRespuesta),
  url(r'^preguntas/$',addPregunta),
  url(r'^actualizar/$',set_registro),
  
  url(r'^modificarperfil/$',modificar_perfil),
  #url(r'^usuario_activo/$',usuario_activo),
  url(r'^lista_usuarios/$',lista_usuarios),

  url(r'^verpreguntas/$',ver_preguntas),
  url(r'^vercategorias/$',ver_categoria),
  url(r'^restringircategoria/$',restringir_categoria),
  url(r'^restringirpregunta/$',restringir_pregunta),
  url(r'^controlarpregunta/$',controlar_preguntas),
  url(r'^detallepreguntas/$',detalle_pregunta),
  url(r'^modificar/(?P<id>\d+)/$',modificar_pregunta,name='modificar_pregunta'),
  url(r'^verdetallepregunta/(?P<id>\d+)/$',ver_detalle,name='ver_detalle'),
  url(r'^eliminarpregunta/(?P<id>\d+)/$',eliminar_pregunta,name='eliminar_pregunta'),
  url(r'^eliminarlistadepreguntas/$',eliminar_lista_preguntas),
  url(r'^crearpartida/$',addPartida),
  url(r'^listapartidas/$',lista_de_partidas),
)