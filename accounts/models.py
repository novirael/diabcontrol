from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class UserProfileManager(models.Manager):
    def get_auth_key(self, user):
        try:
            user_profile = user.userprofile
        except UserProfile.DoesNotExist:
            return None

        return user_profile.auth_key


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    auth_key = models.CharField(max_length=18, default=None, null=True)

    objects = UserProfileManager()
