from __future__ import unicode_literals

from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    patient = models.ForeignKey(User)
    date = models.DateField()
    mood_level = models.IntegerField(default=5)
    has_headaches = models.BooleanField(default=False)
    other_diseases = models.TextField(null=True, default=None)
    verified_by = models.ForeignKey(User, default=None, null=True, blank=True, related_name='verified_by')

    def __str__(self):
        return "{} - {}".format(self.date, self.patient)


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


class GlucoseManager(models.Manager):
    def get_queryset(self):
        queryset = super(GlucoseManager, self).get_queryset()
        return queryset.filter(group='glucose')


class PhysicalActivityManager(models.Manager):
    def get_queryset(self):
        queryset = super(PhysicalActivityManager, self).get_queryset()
        return queryset.filter(group='physical_activity')


class NutritionManager(models.Manager):
    def get_queryset(self):
        queryset = super(NutritionManager, self).get_queryset()
        return queryset.filter(group='nutrition')


class ReportData(models.Model):
    GROUPS = (
        ('glucose', 'Glucose'),
        ('physical_activity', 'Physical Activity'),
        ('nutrition', 'Nutrition'),
    )
    TYPES = (
        # Glucose
        ('glucose', 'Glucose'),

        # Physical Activity
        ('flights_climbed', 'Flights Climbed'),
        ('steps', 'Steps'),
        ('heart_rate', 'Heart Rate'),

        # Nutrition
        ('fat', 'Fat'),
        ('protein', 'Protein'),
        ('carbohydrates', 'Carbohydrates'),
    )

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    patient = models.ForeignKey(User)
    report = models.ForeignKey(Report, null=True, default=None, related_name='data')
    type = models.CharField(max_length=255, choices=TYPES)
    group = models.CharField(max_length=255, null=True, default=None, choices=GROUPS)
    datetime = models.DateTimeField()
    value = models.IntegerField()

    objects = ReportDataManager()
    glucose_measurement = GlucoseManager()
    physical_activity = PhysicalActivityManager()
    nutrition = NutritionManager()

    class Meta:
        ordering = ('datetime',)

