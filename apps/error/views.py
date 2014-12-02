from django.shortcuts import render, render_to_response

from django.template import RequestContext

# Create your views here.

def error_permisos(request):
	return render_to_response("error/error_permisos.html",{},RequestContext(request))


def error_consulta(request):
	return render_to_response("error/error_consulta.html",{},RequestContext(request))


def error_eliminarpregunta(request):
	return render_to_response("error/error_eliminarpregunta.html",{},RequestContext(request))

def error_modificarpregunta(request):
	return render_to_response("error/error_modificarpregunta.html",{},RequestContext(request))

def error_eliminarrespuesta(request):
	return render_to_response("error/error_eliminarrepuesta.html",{},RequestContext(request))

def error_modificarrespuesta(request):
	return render_to_response("error/error_modificarrespuesta.html",{},RequestContext(request))

