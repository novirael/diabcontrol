from django.db import models
from django.conf import settings


class Relationship(models.Model):
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='patients')
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='doctors')
