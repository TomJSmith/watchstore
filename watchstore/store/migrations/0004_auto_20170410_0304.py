# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-10 09:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20170408_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchant_review',
            name='Rating',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]),
        ),
    ]