# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-06-14 22:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=60)),
                ('last_name', models.CharField(max_length=60)),
                ('email', models.EmailField(max_length=60)),
                ('password', models.CharField(max_length=30)),
                ('birthday', models.DateTimeField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
