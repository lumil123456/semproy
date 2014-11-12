# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pregunta', '0002_auto_20141008_0159'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfil',
            name='firt_name',
        ),
        migrations.RemoveField(
            model_name='perfil',
            name='last_name',
        ),
        migrations.AddField(
            model_name='perfil',
            name='pais',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
