# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-07 18:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votations', '0010_auto_20180304_1751'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='votation',
            name='month',
        ),
        migrations.AddField(
            model_name='votation',
            name='active',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='votation',
            name='position',
            field=models.CharField(choices=[('1', 'First'), ('2', 'Second'), ('3', 'Third')], max_length=2, null=True),
        ),
    ]
