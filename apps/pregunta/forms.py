from django import forms
from django.forms import ModelForm
from .models import *
import pdb
from django.forms.extras.widgets import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from captcha.fields import ReCaptchaField

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
	#tipo_partida=forms.ChoiceField(widget=forms.RadioSelect,choices=tipo)
	#seleccionar_categoria=forms.ModelMultipleChoiceField(queryset=categoria.objects.all(),widget=forms.CheckboxSelectMultiple())
	class Meta:
		model=Partida
		exclude=["usuario"]