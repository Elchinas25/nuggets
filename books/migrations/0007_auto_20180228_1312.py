# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-28 12:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_auto_20180228_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='rating_model',
            field=models.OneToOneField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='votations.Rating'),
        ),
    ]