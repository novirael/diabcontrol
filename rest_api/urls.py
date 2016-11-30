# encoding: utf-8
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework.authtoken import views

from rest_api.views import DataView

urlpatterns = [
    url(r'^auth/', views.obtain_auth_token),
    url(r'^data/', DataView.as_view()),
    url(r'^msg', include('msg.urls_api'), name='msg'),
]
