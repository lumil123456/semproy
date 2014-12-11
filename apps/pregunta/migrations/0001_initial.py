# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import triviador.apps.pregunta.thumbs


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Juego_user',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('part_perdido', models.IntegerField()),
                ('part_ganado', models.IntegerField()),
                ('puntuacion', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Partida',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=200)),
                ('jugadores', models.PositiveIntegerField()),
                ('tipo_partida', models.CharField(max_length=200, choices=[(b'public', b'Publico'), (b'private', b'Privado')])),
                ('preguntas', models.CharField(max_length=5, choices=[(b'10', b'10'), (b'20', b'20'), (b'30', b'30'), (b'40', b'40'), (b'50', b'50')])),
                ('tiempo_respuesta', models.CharField(max_length=5, choices=[(b'10', b'10'), (b'15', b'15'), (b'20', b'20'), (b'25', b'25'), (b'30', b'30'), (b'35', b'35'), (b'40', b'40'), (b'45', b'45'), (b'50', b'50'), (b'55', b'55'), (b'60', b'60')])),
                ('seleccionar_categoria', models.ManyToManyField(to='pregunta.Categorias')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pais', models.CharField(max_length=100, null=True)),
                ('avatar', triviador.apps.pregunta.thumbs.ImageWithThumbsField(upload_to=b'img_user')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enunciado', models.CharField(max_length=200)),
                ('respuesta', models.CharField(max_length=150)),
                ('categoria', models.ManyToManyField(to='pregunta.Categorias')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Respuestas_Opcionales',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('resp1', models.CharField(max_length=150)),
                ('resp2', models.CharField(max_length=150)),
                ('resp3', models.CharField(max_length=150)),
                ('pregunta', models.ForeignKey(to='pregunta.Pregunta')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
