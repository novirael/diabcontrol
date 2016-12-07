from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class MessageManager(models.Manager):
    def send_msg(self, sender, receiver, content):
        msg = Message(
            sender=sender,
            receiver=receiver,
            content=content
        )

        msg.save()

        return msg


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='msg_sender')
    receiver = models.ForeignKey(User, related_name='msg_receiver')
    content = models.TextField()
    datetime = models.DateTimeField(auto_now=True)

    objects = MessageManager()
