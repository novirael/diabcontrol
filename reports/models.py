from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Report(models.Model):
    id = models.UUIDField(primary_key=True)
    patient = models.ForeignKey(User)
    date = models.DateField()
    data = models.TextField()
