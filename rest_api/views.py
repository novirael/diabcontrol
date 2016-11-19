# encoding: utf-8
from __future__ import unicode_literals

from rest_framework import authentication
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_api.serializers import ReportSerializer


class DataView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = ReportSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
