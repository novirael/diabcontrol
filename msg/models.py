from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q


class MessageManager(models.Manager):
    def send_msg(self, sender, receiver, content):
        msg = Message(
            sender=sender,
            receiver=receiver,
            content=content
        )

        msg.save()

        return msg

    def conversations(self, user1, user2):
        queryset = self.get_queryset()
        return queryset.filter(
            Q(sender=user1, receiver=user2) |
            Q(sender=user2, receiver=user1)
        )


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='msg_sender')
    receiver = models.ForeignKey(User, related_name='msg_receiver')
    content = models.TextField()
    datetime = models.DateTimeField(auto_now=True)

    objects = MessageManager()

    class Meta:
        ordering = ('datetime',)


class Alert(models.Model):
    user = models.OneToOneField(User)
    content = models.TextField()
