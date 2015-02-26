# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=200)),
                ('user_name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=40)),
                ('ssn', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=200)),
                ('cc_number', models.CharField(max_length=25)),
                ('url', models.CharField(max_length=200)),
           
                ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
