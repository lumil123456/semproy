from django.conf.urls import patterns, include, url
from django.contrib import admin
#admin.autodiscover()
from triviador.apps.pregunta.views import *

from django.conf import settings

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/',include("triviador.apps.pregunta.urls")), 
    url(r'^error/',include("triviador.apps.error.urls")), 
    url(r'^media/(?P<path>.*)$','django.views.static.serve',
    {'document_root':settings.MEDIA_ROOT,}
    ),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
)
