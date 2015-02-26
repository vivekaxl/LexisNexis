# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_auto_20141011_1122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registration',
            name='cc_number',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='password',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='ssn',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='url',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='user_name',
        ),
    ]
