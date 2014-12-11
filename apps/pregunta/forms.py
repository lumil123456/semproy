#encoding:utf-8
from django import forms
from django.forms import ModelForm
from .models import *
import pdb
from django.forms.extras.widgets import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from captcha.fields import ReCaptchaField

from django.forms.extras.widgets import *

tipos=(('public','Publico'),('private','Privado'))
numero_preguntas=(('10','10'),('20','20'),('30','30'),('40','40'),('50','50'))
tiempo=(('10 segundos','10 segundos'),('15 segundos','15 segundos'),('20 segundos','20 segundos'),('25 segundos','25 segundos'),('30 segundos','30 segundos'),('35 segundos','35 segundos'),('40 segundos','40 segundos'),('45 segundos','45 segundos'),('50 segundos','50 segundos'),('55 segundos','55 segundos'),('60 segundos','60 segundos'))
categoria=Categorias.objects.all()

class fcapcha(forms.Form):
	captcha = ReCaptchaField(attrs={'theme' : 'clean'})
	

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ( "username", "email" )

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise ValidationError("Email existente")
		return email

	def clean(self):
		form_data = self.cleaned_data
		if form_data['password'] != form_data['password']:
			self._errors["password"] = "password incorrecto"
			del form_data['password']
		return form_data

    def __init__(self, *args, **kwargs):
		super(UserCreateForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({'class' : 'form-control', 'required': 'required'})
		self.fields['email'].widget.attrs.update({'class' : 'form-control', 'required': 'required'})
		self.fields['password1'].widget.attrs.update({'class' : 'form-control', 'required': 'required'})
		self.fields['password2'].widget.attrs.update({'class' : 'form-control', 'required': 'required'})

class Categorias_Form(ModelForm):
	class Meta:
		model=Categorias
class Pregunta_Form(ModelForm):
	class Meta:
		model=Pregunta
		exclude=["usuario"]
class Respuestas_Opcionales_Form(ModelForm):
	class Meta:
		model=Respuestas_Opcionales
		#exclude=["pregunta"]

class Perfil_Form(ModelForm):
	nombre=forms.CharField(max_length=100)
	apellidos=forms.CharField(max_length=100)
	class Meta:
		model=Perfil
		exclude=['user']

class PartidaForm(ModelForm):
	tipo_partida=forms.ChoiceField(widget=forms.RadioSelect,choices=tipos)
	seleccionar_categoria=forms.ModelMultipleChoiceField(queryset=Categorias.objects.all(),widget=forms.CheckboxSelectMultiple()) 
	
	#tipo_partida=forms.ChoiceField(widget=forms.RadioSelect,choices=tipo)
	#seleccionar_categoria=forms.ModelMultipleChoiceField(queryset=categoria.objects.all(),widget=forms.CheckboxSelectMultiple())
	class Meta:
		model=Partida
		exclude=["usuario"]


class Fcontrasena(forms.Form):
	password1=forms.CharField(widget=forms.PasswordInput(),label="Contraseña antigua")
	password2=forms.CharField(widget=forms.PasswordInput(),label="Contraseña nueva")
	password3=forms.CharField(widget=forms.PasswordInput(),label="Contraseña nueva confirmar")
	def clean(self):
		cleaned_data = super(Fcontrasena,self).clean()
		contrasena2=str(self.cleaned_data.get("password2"))
		contrasena3=str(self.cleaned_data.get("password3"))
		if contrasena2 != contrasena3:
			raise forms.ValidationError("Las contraseñas no coinciden")
		return contrasena2

