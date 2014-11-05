# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import triviador.apps.pregunta.thumbs


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pregunta', '0001_initial'),
    ]

    operations = [
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
                ('Titulo_p', models.CharField(max_length=150)),
                ('Tipo', models.CharField(max_length=15)),
                ('Num_preguntas', models.IntegerField()),
                ('categoria_par', models.ManyToManyField(to='pregunta.Categorias')),
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
                ('firt_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('avatar', triviador.apps.pregunta.thumbs.ImageWithThumbsField(upload_to=b'img_user')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='perfiluser',
            name='user',
        ),
        migrations.DeleteModel(
            name='PerfilUser',
        ),
    ]
