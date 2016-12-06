# encoding: utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from msg.models import Message
from msg.serializers import MessageSenderSerializer, MessageSerializer, UserMessageSerializer


class MessagesListView(APIView):
    def get(self, request, *args, **kwargs):
        is_doctor = self.request.user.groups.filter(name='Doctor').exists()

        if is_doctor:
            doctor = self.request.user
            patient = self.kwargs['user_id']
        else:
            patient = self.request.user
            doctor = self.kwargs['user_id']

        messages = Message.objects.filter(
            doctor=doctor,
            patient=patient
        )

        serializer = MessageSerializer(messages, many=True)

        return Response(serializer.data)


class MessagesConversationListView(APIView):
    def get(self, request, *args, **kwargs):
        is_doctor = self.request.user.groups.filter(name='Doctor').exists()

        if is_doctor:
            messages_owner = Message.objects.get_doctor_conversation_list(self.request.user)
        else:
            messages_owner = Message.objects.get_patient_conversation_list(self.request.user)

        messages_users = [User.objects.get(pk=u_id) for u_id in messages_owner]

        serializer = UserMessageSerializer(messages_users, many=True)

        return Response(serializer.data)


class MessagesNewView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MessageSenderSerializer(data=request.data)

        if serializer.is_valid():
            is_doctor = self.request.user.groups.filter(name='Doctor').exists()

            if is_doctor:
                doctor = self.request.user
                patient = User.objects.get(pk=serializer.validated_data['to_id'])
            else:
                patient = self.request.user
                doctor = User.objects.get(pk=serializer.validated_data['to_id'])

            Message.objects.send_msg(doctor, patient, serializer.validated_data['content'])

            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
