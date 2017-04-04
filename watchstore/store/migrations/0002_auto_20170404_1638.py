# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-04 22:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image', models.URLField()),
                ('Product_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Product')),
            ],
        ),
        migrations.AlterField(
            model_name='credit_card',
            name='FName',
            field=models.CharField(max_length=50, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='credit_card',
            name='LName',
            field=models.CharField(max_length=50, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='credit_card',
            name='Number',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='Credit Card Number'),
        ),
        migrations.AlterField(
            model_name='credit_card',
            name='Security_Code',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='customer',
            name='FName',
            field=models.CharField(max_length=50, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='LName',
            field=models.CharField(max_length=50, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='FName',
            field=models.CharField(max_length=50, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='LName',
            field=models.CharField(max_length=50, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='moderator',
            name='FName',
            field=models.CharField(max_length=50, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='moderator',
            name='LName',
            field=models.CharField(max_length=50, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='moderator',
            name='Resp_Level',
            field=models.CharField(choices=[('HI', 'High'), ('MED', 'Medium'), ('LOW', 'Low')], max_length=50, verbose_name='Responsibility Level'),
        ),
    ]
