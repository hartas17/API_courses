# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-07-29 18:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20180729_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scorestudent',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Students'),
        ),
    ]