from django.db import models
from django.contrib.auth.models import User
from thumbs import ImageWithThumbsField
# Create your models here.
class Categorias(models.Model):
	nombre=models.CharField(max_length=100,unique=True)
	def __unicode__(self):
		return "->%s "%(self.nombre)
class Pregunta(models.Model):
	usuario=models.ForeignKey(User, null=True)
	enunciado=models.CharField(max_length=200)
	respuesta=models.CharField(max_length=150)
	categoria=models.ManyToManyField(Categorias)
	def __unicode__(self):
		return "->%s "%(self.Titulo)
class Respuestas_Opcionales(models.Model):
	resp1=models.CharField(max_length=150)
	resp2=models.CharField(max_length=150)
	resp3=models.CharField(max_length=150)
#	resp4=models.CharField(max_length=150)
	pregunta=models.ForeignKey(Pregunta)
class Juego_user(models.Model):
	part_perdido=models.IntegerField()
	part_ganado=models.IntegerField()
	puntuacion=models.IntegerField()


class Partida(models.Model):
	tipos=(('public','Publico'),('private','Privado'))
	numero_preguntas=(('10','10'),('20','20'),('30','30'),('40','40'),('50','50'))
	tiempo=(('10','10'),('15','15'),('20','20'),('25','25'),('30','30'),('35','35'),('40','40'),('45','45'),('50','50'),('55','55'),('60','60'))
	titulo=models.CharField(max_length=200)
	jugadores=models.PositiveIntegerField()
	tipo_partida=models.CharField(max_length=200,choices=tipos)
	preguntas=models.CharField(max_length=5, choices=numero_preguntas)
	tiempo_respuesta=models.CharField(max_length=5,choices=tiempo)
	seleccionar_categoria=models.ManyToManyField(Categorias, blank=False)
	usuario=models.ForeignKey(User)
	def __unicode__(self):
		return self.titulo
class Perfil(models.Model):
	user=models.OneToOneField(User, unique=True)
	pais=models.CharField(max_length=100, null=True)
	#firt_name=models.CharField(max_length=30)
	#last_name=models.CharField(max_length=30)
	avatar=ImageWithThumbsField(upload_to="img_user", sizes=((50,50),(200,200)))