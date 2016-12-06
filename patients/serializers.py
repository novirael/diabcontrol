# encoding: utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User
from rest_framework import serializers


class RelationshipUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')
