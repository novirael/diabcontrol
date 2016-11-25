from django.conf import settings
from django.db import models


class Invitation(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='doctor_invitations'
    )
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='patient_invitations'
    )
    is_accepted = models.BooleanField(default=False)
