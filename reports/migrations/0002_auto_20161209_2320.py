# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-09 23:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportdata',
            name='group',
            field=models.CharField(choices=[('glucose', 'Glucose'), ('physical_activity', 'Physical Activity'), ('nutrition', 'Nutrition')], default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='reportdata',
            name='type',
            field=models.CharField(choices=[('glucose', 'Glucose'), ('flights_climbed', 'Flights Climbed'), ('steps', 'Steps'), ('heart_rate', 'Heart Rate'), ('fat', 'Fat'), ('protein', 'Protein'), ('carbohydrates', 'Carbohydrates')], max_length=255),
        ),
    ]
