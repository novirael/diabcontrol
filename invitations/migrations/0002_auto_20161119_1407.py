# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.auth.models import User, Group


TEST_USERS = (
        'doctor_a',
        'doctor_b',
        'patient_a',
        'patient_b',
    )


def forward(apps, schema_editor):
    patient_group = Group.objects.create(name='Patient')
    doctor_group = Group.objects.create(name='Doctor')

    for user in TEST_USERS:
        first_name, last_name = map(lambda x: x.title(), user.split('_'))
        username = user + '@example.com'
        u = User(
            username=username,
            email=username,
            first_name=first_name,
            last_name=last_name,
        )
        u.set_password('admin123')
        u.save()

        u.groups.add(doctor_group if 'doctor' in username else patient_group)


def backward(apps, schema_editor):
    Group.objects.filter(name__in=('Patient', 'Doctor')).delete()

    User.objects.filter(
        username__in=map(lambda x: x + '@example.com', TEST_USERS)
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('invitations', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
