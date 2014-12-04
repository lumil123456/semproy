# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pregunta', '0007_remove_respuestas_opcionales_resp4'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorias',
            name='nombre',
            field=models.CharField(unique=True, max_length=100),
        ),
    ]
