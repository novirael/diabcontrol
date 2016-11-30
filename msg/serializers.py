# encoding: utf-8
from __future__ import unicode_literals

from rest_framework import serializers

from msg.models import Message


class MessageSerializer(serializers.Serializer):
    doctor_id = serializers.IntegerField()
    patient_id = serializers.IntegerField()
    content = serializers.CharField()
    datetime = serializers.DateTimeField(read_only=True)


class MessageSerializerModel(serializers.ModelSerializer):
    datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Message
        fields = ('doctor_id', 'patient_id', 'content', 'datetime')
