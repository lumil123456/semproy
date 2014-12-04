# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pregunta', '0008_auto_20141203_0904'),
    ]

    operations = [
        migrations.RenameField(
            model_name='perfil',
            old_name='pais',
            new_name='departamento',
        ),
    ]
