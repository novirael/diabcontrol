# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-07 22:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('msg', '0002_auto_20161207_2226'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='doctor',
            new_name='sender'
        ),
        migrations.RenameField(
            model_name='message',
            old_name='patient',
            new_name='receiver'
        )
    ]
