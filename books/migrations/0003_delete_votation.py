# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-26 13:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_votation'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Votation',
        ),
    ]
