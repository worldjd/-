# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-20 14:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myuser', '0004_user_sex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='home',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='school',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.SmallIntegerField(blank=True, choices=[(1, '男'), (2, '女'), (3, '保密')], default=3),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]