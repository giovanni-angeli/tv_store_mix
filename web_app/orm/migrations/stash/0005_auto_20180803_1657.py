# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-03 14:57
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('orm', '0004_auto_20180803_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tvstoreunit',
            name='deletion_date',
            field=models.DateTimeField(default=datetime.datetime(2028, 8, 2, 14, 57, 32, 372008, tzinfo=utc)),
        ),
    ]
