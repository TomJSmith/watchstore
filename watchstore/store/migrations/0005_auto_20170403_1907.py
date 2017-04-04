# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-04 01:07
from __future__ import unicode_literals

import address.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0001_initial'),
        ('store', '0004_auto_20170403_1853'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('Order_Number', models.AutoField(primary_key=True, serialize=False)),
                ('Total_Price', models.DecimalField(decimal_places=2, default=0.0, max_digits=19)),
                ('Billing_Info', address.models.AddressField(on_delete=django.db.models.deletion.CASCADE, related_name='bank_info', to='address.Address')),
                ('Placed_By', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Customer')),
                ('Shipping_Info', address.models.AddressField(on_delete=django.db.models.deletion.CASCADE, related_name='shipping_info', to='address.Address')),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='ID',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='Price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=19),
        ),
    ]