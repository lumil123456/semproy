from .forms import *
from .models import *
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect

from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext, loader, Context, Template
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse 
from django.http import *
from .models import *

#from django.conf import settings
#from django.core.mail import send_mail
#from django.views.generic import FormView
#from myapp.forms import ContactForm

def pagina_index(request):
	return render_to_response("blog/index.html",{},context_instance=RequestContext(request))
def registro(request):
	username = password = email =''
	if request.method=="POST":
		user_form = UserCreateForm(request.POST)
		if user_form.is_valid():
			nuevo_usuario=user_form.save()
			#No es necesario
			#usuario = User(username=request.POST['username'], email=request.POST['email'])
			#usuario.set_password(request.POST['password1'])
			#creamos el perfil
			perfil=Perfil.objects.create(user=nuevo_usuario)
			#usuario.save()
			return HttpResponseRedirect("/blog/login")
	else:
		user_form = UserCreateForm()

	diccionario = {
		'user_form': user_form,
		'page_title': 'Aplicacion - Register',
		'body_class': 'register',
	}
	return render_to_response("usuario/registro.html", diccionario, context_instance=RequestContext(request))
def login_usuario(request):
	if request.method=="POST":
		form=AuthenticationForm(request.POST)
		if request.session['cont']>3:
			form2=fcapcha(request.POST)
			if form2.is_valid():
				pass
			else:
				datos={'form':form,'form2':form2}
				return render_to_response("usuario/login.html",datos,context_instance=RequestContext(request))		
		if(form.is_valid()==False):
			username=request.POST["username"]
			password=request.POST["password"]
			resultado=authenticate(username=username,password=password)
			if resultado:
				login(request,resultado)
				request.session["name"]=username
				return HttpResponseRedirect("/blog/perfil/")
			else:
				request.session['cont']=request.session['cont']+1
				aux=request.session['cont']
				estado=True
				mensaje="Error en los datos "+str(aux)
				if aux>3:
					form2=fcapcha()
					datos={'form':form,'form2':form2,'estado':estado,'mensaje':mensaje}
				else:
					datos={'form':form,'estado':estado,'mensaje':mensaje}
				return render_to_response("usuario/login.html",datos,context_instance=RequestContext(request))	
	else:
		request.session['cont']=0
		form=AuthenticationForm()
	return render_to_response("usuario/login.html",{"form":form},RequestContext(request))

def logout_usuario(request):
	logout(request)
	return HttpResponseRedirect("/blog/")
def perfil(request):
	return render_to_response("usuario/perfil.html",{"nombre":request.session["name"]},RequestContext(request))
def perfil_agregar(request):
	if request.user.is_authenticated():
		usuario=User.objects.get(username=request.user)
		perfil=Perfil.objects.get(user=usuario)
		if request.method=="POST":
			formulario=Perfil_Form(request.POST,request.FILES,instance=perfil)
			if formulario.is_valid():
				nombre=request.POST['nombre']
				apellido=request.POST['apellidos']
				formulario.save()
				usuario.first_name=nombre
				usuario.last_name=apellido
				usuario.save()
				return HttpResponseRedirect("/blog/perfil/")
		else:
			formulario=Perfil_Form(instance=perfil,data={'nombre':usuario.first_name,'apellidos':usuario.last_name})
		return render_to_response("usuario/perfil_agregar.html",{"formulario":formulario},context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect("/usuario/login/")
def lista_usuarios(request):
	usuarios=User.objects.all()
	return render_to_response("usuario/lista_usuarios.html",{"usuarios":usuarios},context_instance=RequestContext(request))
def addCategoria(request):
	usuario=request.user
	if(not usuario.has_perm("usuario.addCategoria")):
		return HttpResponseRedirect("/error/permit")
	if(request.method=="POST"):
		form_cat=Categorias_Form(request.POST)
		if(form_cat.is_valid()):
			form_cat.save()
			return HttpResponseRedirect("/blog/categoria/")
	form_cat=Categorias_Form()
	return render_to_response("blog/categorias.html",{"form":form_cat},RequestContext(request))
def addPregunta(request):
	usuario=request.user
	if(not usuario.has_perm("usuario.addPregunta")):
		return HttpResponseRedirect("/error/permit")
	if(request.method=="POST"):
		form_pre=Pregunta_Form(request.POST)
		if(form_pre.is_valid()):
			form_pre.save()
			return HttpResponseRedirect("/blog/preguntas/")
	form_pre=Pregunta_Form()
	return render_to_response("blog/preguntas.html",{"form":form_pre},RequestContext(request))


def addRespuesta(request):
	usuario=request.user
	if(not usuario.has_perm("usuario.addRespuesta")):
		return HttpResponseRedirect("/error/permit")
	if(request.method=="POST"):
		form_res=Respuestas_Opcionales_Form(request.POST)
		if(form_res.is_valid()):
			form_res.save()
			return HttpResponseRedirect("/blog/respuestas/")
	form_res=Respuestas_Opcionales_Form()
	return render_to_response("blog/respuestas.html",{"form":form_res},RequestContext(request))


@login_required
def set_registro(request):
	if request.method=="POST":
		formulario_registro=Perfil_Form(request.POST)
		if formulario_registro.is_valid():
			formulario_registro.save()
			return HttpResponseRedirect("/login/")
	else:
		formulario_registro=Perfil_Form()
	return render_to_response("usuario/setregistro.html",{'form':formulario_registro},context_instance=RequestContext(request))
#para verificar si un usuario esta activo
def user_active_view(request):
	if request.user.is_authenticated():
		usuario=request.user
		if usuario.is_active:
			return HttpResponseRedirect("/user/perfil/")
		else:
			if request.method=="POST":
				u=User.objects.get(username=usuario)
				perfil=Perfil.objects.get(user=u)
				formulario=fperfil(request.POST,request.FILES,instance=perfil)
				if formulario.is_valid():
					formulario.save()
					u.is_active=True
					u.save()
					return HttpResponseRedirect("/user/perfil/")
			else:
				formulario=fperfil()
			return render_to_response("usuario/activar.html",{'formulario':formulario},context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect("/login/")
#modificar perfil no me muestra
def modificar_perfil(request):
	if request.user.is_authenticated():
		a=request.user
		usuario=User.objects.get(username=a)
		perfil=Perfil.objects.get(user=usuario)
		if request.method=='POST':
			formulario=fperfil_modificar(request.POST,request.FILES,instance=perfil)
			if formulario.is_valid():
				formulario.save()
				return HttpResponseRedirect("/usuario/perfil/"+str(usuario.id)+"/")
		else:
			formulario=fperfil_modificar(instance=perfil)
			return render_to_response('modificar_perfil.html',{'formulario':formulario},context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect("/login/")
def listar_usuario(request):
	usuarios=User.objects.all()
	return render_to_response("blog/listar_usuario.html",{"usuarios":usuarios},context_instance=RequestContext(request))
#def permisos(request):
#	listadepermisos=[]
#	if(request.user.has_perm("usuarios.addCategoria")):
#		listadepermisos.append("url":"/blog/categorias","label":"Categorias")
#	if(request.user.has_perm("usuarios.addPregunta")):
#		listadepermisos.append("url":"/blog/pregunta","label":"Pregunta")
#	if(request.user.has_perm("usuarios.addRespuesta")):
#		listadepermisos.append("url":"/blog/respuestas","label":"Respuestas")
#	if(request.user.has_perm("usuarios.ver_blog")):
#		listadepermisos.append("url":"/blog/addcrearpartida","label":"blog")
#	listadepermisos.append({"url":"/blog/","label":"Registro"})
#	listadepermisos.append({"url":"/blog/","label":"Login"})
# 	return listadepermisos

#preguntas

def ver_preguntas(request):
	lista=Pregunta.objects.all()
	return render_to_response("blog/ver_preguntas.html",{"lista":lista},RequestContext(request))
def restringir_categoria(request):
	lista=categoria.objects.all()
	return render_to_response("blog/restringir_categoria.html",{"categoria":categoria},RequestContext(request))
def restringir_pregunta(request):
	lista=pregunta.objects.all()
	return render_to_response("blog/restringir_pregunta.html",{"lista":lista},RequestContext(request))
def ver_categoria(request):
	lista=categorias.objects.all()
	return render_to_response("blog/ver_categoria.html",{"lista":lista},RequestContext(request))
def controlar_preguntas(request):
	lista=pregunta.objects.all()
	return render_to_response("blog/controlar_preguntas.html",{"lista":lista},RequestContext(request))

def modificar_pregunta(request,id):
	pregunta=Pregunta.objects.get(pk=id)
	if request.method=="POST":
		fpregunta=Pregunta_Form(request.POST, instance=pregunta)
		if fpregunta.is_valid():
			fpregunta.save()
			return HttpResponse("pregunta modificada")
	else:
		fpregunta=Pregunta_Form(instance=pregunta)
	return render_to_response("blog/modificar_pregunta.html",{"fpregunta":fpregunta},RequestContext(request))
#error desde aki hasta
def detalle_pregunta(request):
	pregunta=get_object_or_404(Pregunta,pk=pregunta)
	return render_to_response("blog/detalle_pregunta.html",{"pregunta":pregunta},RequestContext(request))
def ver_detalle(request,id):
	pregunta=get_object_or_404(mpregunta,pk=id)
	return render_to_response("blog/ver_detalle.html",{"pregunta":pregunta},RequestContext(request))

def ver_detalle_prgunta(request,id):
	pregunta=get_object_or_404(pregunta, pk=id)
	return render_to_response("blog/ver_detalle.html",{"pregunta":pregunta},RequestContext(request))
#eeror al eliminar 
def eliminar_pregunta(request,id):
	elim=pregunta.objects.get(pk=id)
	borrar=elim.delete()
	return render_to_response("/blog/eliminar_pregunta/")
def eliminar_lista_preguntas(request):
	lista=pregunta.objects.all()
	return render_to_response("blog/eliminar_lista_preguntas.html",{"lista":lista},RequestContext(request))
#hasta aki
def addPartida(request):
	if(request.method=="POST"):
		usuario=User.objects.get(username=request.user)
		form=PartidaForm(request.POST)
		if(form.is_valid()):
			obj=form.save(commit=False)
			obj.usuario=usuario
			obj.save()
			form.save_m2m()
			return HttpResponseRedirect("/trivia/")
	else:
		form=PartidaForm()
	return render_to_response("blog/addPartida.html",{"form":form},RequestContext(request))
def lista_de_partidas(request):
	lista=Partida.objects.filter(tipo_partida='public')
	return render_to_response("blog/lista_de_partidas.html",{"lista":lista},RequestContext(request))
