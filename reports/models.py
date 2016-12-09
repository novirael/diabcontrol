from __future__ import unicode_literals

from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models


class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    patient = models.ForeignKey(User)
    date = models.DateField(auto_now=True)
    mood_level = models.IntegerField(default=5)
    has_headaches = models.BooleanField(default=False)
    other_diseases = models.TextField(null=True, default=None)


class ReportDataManager(models.Manager):
    def save_data(self, patient, data_type, datetime, value, group=None, report=None):
        return self.create(
            patient=patient,
            report=report,
            type=data_type,
            group=group,
            datetime=datetime,
            value=value
        )


class ReportData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    patient = models.ForeignKey(User)
    report = models.ForeignKey(Report, null=True, default=None, related_name='data')
    type = models.CharField(max_length=255)
    group = models.CharField(max_length=255, null=True, default=None)
    datetime = models.DateTimeField()
    value = models.IntegerField()

    objects = ReportDataManager()
