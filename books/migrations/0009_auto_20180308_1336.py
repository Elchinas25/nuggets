# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-08 12:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_auto_20180302_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='rating_model',
            field=models.OneToOneField(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='votations.Rating'),
        ),
    ]
