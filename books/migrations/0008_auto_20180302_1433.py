# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-02 13:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_auto_20180228_1312'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['-rating_model__average']},
        ),
    ]
