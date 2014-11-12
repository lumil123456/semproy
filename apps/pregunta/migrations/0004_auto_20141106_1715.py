# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pregunta', '0003_auto_20141106_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='pais',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
