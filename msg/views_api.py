# encoding: utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from msg.models import Message
from msg.serializers import MessageSenderSerializer, MessageSerializer, UserMessageSerializer


class MessagesListView(APIView):
    def get(self, request, *args, **kwargs):
        messages = Message.objects.filter(
            Q(
                sender=self.request.user,
                receiver=self.kwargs['user_id'],
            ) |
            Q(
                sender=self.kwargs['user_id'],
                receiver=self.request.user,
            )
        )
        serializer = MessageSerializer(messages, many=True)

        return Response(serializer.data)


class MessagesNewView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MessageSenderSerializer(data=request.data)

        if serializer.is_valid():
            receiver_id = serializer.validated_data['to_id']
            Message.objects.send_msg(
                self.request.user,
                User.objects.get(pk=receiver_id),
                serializer.validated_data['content']
            )
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
