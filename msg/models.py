from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    doctor = models.ForeignKey(User, related_name='main_doctor')
    patient = models.ForeignKey(User, related_name='main_patient')
    content = models.TextField()
    datetime = models.DateTimeField(auto_now=True)
