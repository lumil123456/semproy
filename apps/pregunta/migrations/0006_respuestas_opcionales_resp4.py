# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pregunta', '0005_perfil_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='respuestas_opcionales',
            name='resp4',
            field=models.CharField(default='prueba', max_length=150),
            preserve_default=False,
        ),
    ]
