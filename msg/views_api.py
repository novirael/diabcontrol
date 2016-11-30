# encoding: utf-8
from __future__ import unicode_literals

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from msg.models import Message
from msg.serializers import MessageSerializer


class MessagesListView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        is_doctor = self.request.user.groups.filter(name='Doctor').exists()

        if not is_doctor:
            qs = Message.objects.filter(
                doctor_id=user_id
            )

        else:
            qs = Message.objects.filter(
                patient_id=user_id
            )

        qs = qs.order_by('datetime')

        serializer = MessageSerializer(qs, many=True)

        return Response(serializer.data)


class MessagesNewView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)

        if serializer.is_valid():
            msg = Message(
                doctor_id=serializer.validated_data['doctor_id'],
                patient_id=serializer.validated_data['patient_id'],
                content=serializer.validated_data['content']
            )

            msg.save()

            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
