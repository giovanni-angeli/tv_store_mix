# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-03 19:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orm', '0014_tvstorecontact_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='tvstoreunit',
            name='ftp_url',
            field=models.CharField(default='ftp://1.1.1.1/metusco', max_length=200, verbose_name='ftp_url'),
        ),
    ]
