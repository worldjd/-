# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-19 20:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myuser', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=50),
        ),
    ]
