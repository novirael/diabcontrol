from django.conf import settings
from django.db import models


class InvitationManager(models.Manager):
    def get_active(self, doctor):
        qs = self.all().filter(
            doctor=doctor,
            is_accepted=True,
        )

        return qs


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

    objects = InvitationManager()
