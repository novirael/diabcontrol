# encoding: utf-8
from __future__ import unicode_literals

from rest_framework import serializers

from reports.models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('id', 'patient', 'date', 'data')
