# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-24 15:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0005_submission_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='code',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
