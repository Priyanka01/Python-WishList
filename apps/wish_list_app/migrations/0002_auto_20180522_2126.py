# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-22 21:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wish_list_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]