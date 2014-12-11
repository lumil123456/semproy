from .forms import *
from .models import *
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect,HttpResponse

from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext, loader, Context, Template
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse 
from django.http import *
from .models import *
from django.contrib.sessions.backends.db import SessionStore

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
			if resultado is not None: # NODE JS
				if resultado.is_active:
					login(request,resultado)
					p=SessionStore()
					p["name"]=username
					p["estado"]="conectado"
					p.save()
					request.session["idkey"]=p.session_key
					del request.session['cont']
					#return HttpResponseRedirect("/perfil/")
					request.session["name"]=username
					return HttpResponseRedirect("/blog/perfil/")
				else:
					login(request, resultado)
					return HttpResponseRedirect("/activar/")
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
	p=SessionStore(session_key=request.session["idkey"])
	p["estado"]="desconectado"
	p["name"]=""
	p.save()
	logout(request)
	return HttpResponseRedirect("/blog/")

def cambiar_contrasena(request):
	if request.method=="POST":
		formulario=Fcontrasena(request.POST)
		if formulario.is_valid():
			contrasena_antigua=request.POST['password1']
			contrasena_nueva=request.POST['password2']
			#contrasena_antigua=request.POST['password1']
			resultado=authenticate(username=request.user,password=contrasena_antigua)
			if resultado is not None:
				usuario=User.objects.get(username=request.user)
				usuario.set_password(contrasena_nueva)
				usuario.save()
				#login(request,resultado)
				return HttpResponseRedirect("/blog/login/")
			else:
				return HttpResponse("La contrasena no coincide con la antigua")
	else:
		formulario=Fcontrasena()
	return render_to_response("usuario/contrasena.html",{'formulario':formulario},RequestContext(request))

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
	titulo="Registro de categoria"
	categoria=Categorias.objects.all()
	usuario=request.user
	if(not usuario.has_perm("usuario.addCategoria")):
		return render_to_response("blog/restringir_categoria.html",{},RequestContext(request))
	if request.method=="POST":
		formulario=Categorias_Form(request.POST)
		if formulario.is_valid():
			formulario.save()
			estado=True
			datos={'titulo':titulo,'formulario':formulario,'estado':estado,'categoria':categoria}
			return render_to_response("blog/categorias.html",datos,context_instance=RequestContext(request))
	else:
		formulario=Categorias_Form()
	datos={'titulo':titulo,'formulario':formulario,'categoria':categoria}
	return render_to_response("blog/categorias.html",datos,context_instance=RequestContext(request))
def addPregunta(request):
	usuario=request.user
	if(not usuario.has_perm("usuario.addPregunta")):
		return render_to_response("blog/restringir_pregunta.html",{},RequestContext(request))
	if(request.method=="POST"):
		form_pre=Pregunta_Form(request.POST)
		if(form_pre.is_valid()):
			form_pre.save()
			#form_pre.save_m2m()
			return HttpResponseRedirect("/blog/preguntas/")
	form_pre=Pregunta_Form()
	return render_to_response("blog/preguntas.html",{"form":form_pre},RequestContext(request))
def addRespuesta(request):
	usuario=request.user
	if(not usuario.has_perm("usuario.addRespuesta")):
		return render_to_response("blog/restringir_respuestas.html",{},RequestContext(request))
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
	usuario=request.user
	if(not usuario.has_perm("usuario.addCategoria")):
		return render_to_response("blog/restringir_categoria.html",{},RequestContext(request))
	lista=Pregunta.objects.all()
	lista2=Respuestas_Opcionales.objects.all()
	return render_to_response("blog/ver_preguntas.html",{"lista":lista,'lista2':lista2},RequestContext(request))
def restringir_categoria(request):
	lista=Categorias.objects.all()
	return render_to_response("blog/restringir_categoria.html",{"lista":lista},RequestContext(request))
def restringir_pregunta(request):
	lista=Pregunta.objects.all()
	return render_to_response("blog/restringir_pregunta.html",{"lista":lista},RequestContext(request))
def ver_categoria(request):
	usuario=request.user
	if(not usuario.has_perm("usuario.addCategoria")):
		return render_to_response("blog/restringir_categoria.html",{},RequestContext(request))
	lista=categorias.objects.all()
	return render_to_response("blog/ver_categoria.html",{"lista":lista},RequestContext(request))
def controlar_preguntas(request):
	usuario=request.user
	if(not usuario.has_perm("usuario.addCategoria")):
		return render_to_response("blog/restringir_categoria.html",{},RequestContext(request))
	lista=pregunta.objects.all()
	return render_to_response("blog/controlar_preguntas.html",{"lista":lista},RequestContext(request))

def modificar_pregunta(request,id):
	usuario=request.user
	if(not usuario.has_perm("usuario.addCategoria")):
		return render_to_response("blog/restringir_categoria.html",{},RequestContext(request))
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
	usuario=request.user
	if(not usuario.has_perm("usuario.addCategoria")):
		return render_to_response("blog/restringir_categoria.html",{},RequestContext(request))
	pregunta=get_object_or_404(Pregunta,pk=pregunta)
	return render_to_response("blog/detalle_pregunta.html",{"pregunta":pregunta},RequestContext(request))
def ver_detalle(request,id):
	usuario=request.user
	if(not usuario.has_perm("usuario.addCategoria")):
		return render_to_response("blog/restringir_categoria.html",{},RequestContext(request))
	pregunta=get_object_or_404(mpregunta,pk=id)
	return render_to_response("blog/ver_detalle.html",{"pregunta":pregunta},RequestContext(request))

def ver_detalle_pregunta(request,id):
	usuario=request.user
	if(not usuario.has_perm("usuario.addCategoria")):
		return render_to_response("blog/restringir_categoria.html",{},RequestContext(request))
	pregunta=get_object_or_404(pregunta, pk=id)
	return render_to_response("blog/ver_detalle.html",{"pregunta":pregunta},RequestContext(request))
#eeror al eliminar 
def eliminar_pregunta(request,id):
	usuario=request.user
	if(not usuario.has_perm("usuario.addCategoria")):
		return render_to_response("blog/restringir_categoria.html",{},RequestContext(request))
	elim=Pregunta.objects.get(pk=id)
	borrar=elim.delete()
	return HttpResponseRedirect("/blog/eliminarlistadepreguntas/")
#esto ya funciona
def eliminar_lista_preguntas(request):
	usuario=request.user
	if(not usuario.has_perm("usuario.addCategoria")):
		return render_to_response("blog/restringir_categoria.html",{},RequestContext(request))
	lista=Pregunta.objects.all()
	return render_to_response("blog/eliminar_lista_preguntas.html",{"lista":lista},RequestContext(request))
#hasta aki
def crear_partida(request):
	if(request.method=="POST"):
		usuario=User.objects.get(username=request.user)
		form=PartidaForm(request.POST)
		if(form.is_valid()):
			obj=form.save(commit=False)
			obj.usuario=usuario
			obj.save()
			form.save_m2m()
			return HttpResponseRedirect("/blog/")
	else:
		form=PartidaForm()
	return render_to_response("blog/crear_partida.html",{"form":form},RequestContext(request))
def lista_de_partidas(request):
	lista=Partida.objects.filter(tipo_partida='public')
	return render_to_response("blog/lista_de_partidas.html",{"lista":lista},RequestContext(request))

def gamer_view(request):
	idsession=request.session["idkey"]
	return HttpResponseRedirect("http://localhost:3006/?id_session="+idsession)

def chat(request):
	idsession=request.session["idkey"]
	return HttpResponseRedirect("http://localhost:3006/django/"+idsession)


#def permisos(request):
#	listadepermisos=[]
#	listadepermisos.append({"url":"/blog/game/","label":"Game"})
	#listadepermisos.append({"url":"/blog/login/","label":"Login"})
	#listadepermisos.append({"url":"/blog/logout/","label":"LoginOUT"})
#	return listadepermisos	
#def adminPermisos(request):
#	permisosGlobales=mispermisos()
#	lista=permisos(request)
#	render_to_response("")
#myuser.permissions.add("")
#myuser.premissions.remove("")
#def mispermisos():
#	listagenerica=[]
#	listagenerica.append({"id":"usuarios.blog"})
#	return listagenerica

#def permisos(request):
#	listadepermisos=[]
#	if(request.user.has_perm("usuarios.ver_blog")):
#		listadepermisos.append({"url":"/blog/","label":"Blog"})
#	if request.user.has_perm("usuarios.addCategoria"):
#		listadepermisos.append({"url":"/blog/categorias/","label":"Categorias"})
#	if request.user.has_perm("usuarios.addPregunta"):
#		listadepermisos.append({"url":"/blog/preguntas/","label":"Pregunta"})
#	if request.user.has_perm("usuarios.addRespuesta"):
#		listadepermisos.append({"url":"/blog/respuestas/","label":"Pregunta"})
#	listadepermisos.append({"url":"/blog/registro/","label":"Registro"})
#	listadepermisos.append({"url":"/blog/nuevapartida/","label":"Nueva Partida"})
	#listadepermisos.append({"url":"/blog/login/","label":"Login"})
	#listadepermisos.append({"url":"/blog/logout/","label":"LoginOUT"})
#	return listadepermisos	


#def adminPermisos(request):
#	permisosGlobales=mispermisos()
#	lista=permisos(request)
#	render_to_response("")
#myuser.permissions.add("")
#myuser.premissions.remove("")
#def mispermisos():
#	listagenerica=[]
#	listagenerica.append({"id":"usuarios.ver_blog"})
#	listagenerica.append({"id":"usuarios.categoria"})
#	listagenerica.append({"id":"usuarios.addPregunta"})
#	listagenerica.append({"id":"usuarios.addRespuesta"})
#	listagenerica.append({"id":"usuarios.addCategoria"})
#	return listagenerica

#def bienvenidofb(request):
#	return HttpResponseRedirect("/trivia/")
#	return render_to_response("bienvenidofb.html",{"menu":menu},RequestContext(request))


#def crear_pregunta(request):

#	if request.method=="POST":
#		fpregunta=Pregunta_Form(request.POST)
#		if fpregunta.is_valid():
#			fpregunta.save()
#			return HttpResponseRedirect("/blog/preguntas/")
#	fpregunta=Pregunta_Form()
#	return render_to_response("blog/crear_pregunta.html",{"fpregunta":fpregunta},RequestContext(request))

def pagina_index(request):
	lista=Partida.objects.filter(tipo_partida='public')
	return render_to_response("blog/index.html",{'lista':lista},context_instance=RequestContext(request))