from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class MessageManager(models.Manager):
    def send_msg(self, doctor, patient, content):
        msg = Message(
            patient=patient,
            doctor=doctor,
            content=content
        )

        msg.save()

        return msg

    def get_doctor_msgs(self, doctor):
        qs = self.filter(
            doctor=doctor
        ).order_by('datetime')

        return qs

    def get_patient_msgs(self, patient):
        qs = self.filter(
            patinent=patient
        ).order_by('datetime')

        return qs

    def get_doctor_conversation_list(self, doctor):
        conversation_list = self.filter(
            doctor=doctor,
        )\
            .values_list('patient', flat=True) \
            .order_by('datetime')

        return conversation_list

    def get_patient_conversation_list(self, patient):
        conversation_list = self.filter(
            patient=patient,
        )\
            .values_list('doctor', flat=True) \
            .order_by('datetime')

        return conversation_list


class Message(models.Model):
    doctor = models.ForeignKey(User, related_name='main_doctor')
    patient = models.ForeignKey(User, related_name='main_patient')
    content = models.TextField()
    datetime = models.DateTimeField(auto_now=True)

    objects = MessageManager()
