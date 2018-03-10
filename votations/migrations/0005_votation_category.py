# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-02 13:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_auto_20180302_1433'),
        ('votations', '0004_rating_ratings'),
    ]

    operations = [
        migrations.AddField(
            model_name='votation',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='books.Category'),
        ),
    ]
