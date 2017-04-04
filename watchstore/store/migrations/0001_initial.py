# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-03 22:53
from __future__ import unicode_literals

import address.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('Email', models.EmailField(max_length=50, primary_key=True, serialize=False)),
                ('Password', models.CharField(max_length=50)),
                ('FName', models.CharField(max_length=50)),
                ('LName', models.CharField(max_length=50)),
                ('Address', address.models.AddressField(on_delete=django.db.models.deletion.CASCADE, to='address.Address')),
            ],
        ),
    ]