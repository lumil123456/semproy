# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pregunta', '0009_auto_20141203_0924'),
    ]

    operations = [
        migrations.RenameField(
            model_name='perfil',
            old_name='departamento',
            new_name='pais',
        ),
    ]
