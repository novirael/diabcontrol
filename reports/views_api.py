# encoding: utf-8
from __future__ import unicode_literals

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from reports.models import Report, ReportData
from reports.serializers import MainReportSerializer


class DataView(APIView):
    def post(self, request):
        serializer = MainReportSerializer(data=request.data)

        if serializer.is_valid():
            data_questions = serializer.data['questions']
            data_stats = serializer.data['stats']

            report = Report()
            report.patient = self.request.user
            report.has_headaches = data_questions['has_headaches']
            report.mood_level = data_questions['mood_level']
            report.other_diseases = data_questions['other_diseases']

            report.save()

            for group, group_data in data_stats.items():
                for data_type, type_data in group_data.items():
                    for data in type_data:
                        ReportData.objects.save_data(
                            self.request.user,
                            data_type,
                            data['timestamp'],
                            data['value'],
                            group,
                            report
                        )

            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
