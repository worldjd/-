# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-25 10:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20181124_0854'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='Activity_add_time',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='添加时间'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activity',
            name='Activity_is_delete',
            field=models.BooleanField(default=False, verbose_name='是否删除'),
        ),
        migrations.AddField(
            model_name='activity',
            name='Activity_revise_time',
            field=models.DateField(auto_now=True, verbose_name='修改时间'),
        ),
    ]
