# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-17 10:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reports', '0003_auto_20161210_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='verified_by',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='verified_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
