# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-08 12:36
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votations', '0011_auto_20180307_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='votation',
            name='puntuations',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
