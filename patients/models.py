from django.conf import settings
from django.db import models


class RelationshipManager(models.Manager):
    def get_doctor_relations(self, doctor):
        relations = self.filter(
            doctor=doctor
        )

        return [r.patient for r in relations]

    def get_patient_relations(self, patient):
        relations = self.filter(
            patient=patient
        )

        return [r.doctor for r in relations]


class Relationship(models.Model):
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='patients')
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='doctors')

    objects = RelationshipManager()
