# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pregunta', '0006_respuestas_opcionales_resp4'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='respuestas_opcionales',
            name='resp4',
        ),
    ]
