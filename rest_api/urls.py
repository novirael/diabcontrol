# encoding: utf-8
from __future__ import unicode_literals

from django.conf.urls import url
from rest_framework.authtoken import views


urlpatterns = [
    url(r'^auth/', views.obtain_auth_token)
]
