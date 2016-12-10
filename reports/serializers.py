# encoding: utf-8
from __future__ import unicode_literals

from rest_framework import serializers


class BaseDataSerializer(serializers.Serializer):
    value = serializers.IntegerField()
    timestamp = serializers.DateTimeField()


class StatsNutritionSerializer(serializers.Serializer):
    fat = BaseDataSerializer(many=True)
    protein = BaseDataSerializer(many=True)
    carbohydrates = BaseDataSerializer(many=True)


class StatsPhysicalActivitySerializer(serializers.Serializer):
    flights_climbed = BaseDataSerializer(many=True)
    steps = BaseDataSerializer(many=True)
    heart_rate = BaseDataSerializer(many=True)


class StatsGlucoseSerializer(serializers.Serializer):
    glucose = BaseDataSerializer(many=True)


class MainStatsSerializer(serializers.Serializer):
    nutrition = StatsNutritionSerializer()
    physical_activity = StatsPhysicalActivitySerializer()


class ReportSerializer(serializers.Serializer):
    has_headaches = serializers.BooleanField()
    mood_level = serializers.IntegerField(min_value=1, max_value=10)
    other_diseases = serializers.CharField(allow_null=True, allow_blank=True)


class MainReportSerializer(serializers.Serializer):
    questions = ReportSerializer()
    stats = MainStatsSerializer()
