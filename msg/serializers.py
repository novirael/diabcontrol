# encoding: utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User
from rest_framework import serializers

from msg.models import Message


class MessageSenderSerializer(serializers.Serializer):
    to_id = serializers.IntegerField()
    content = serializers.CharField()
    datetime = serializers.DateTimeField(read_only=True)


class UserMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')


class MessageSerializer(serializers.ModelSerializer):
    doctor = UserMessageSerializer()
    patient = UserMessageSerializer()

    class Meta:
        model = Message
        fields = ('doctor', 'patient', 'content', 'datetime')
