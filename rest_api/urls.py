# encoding: utf-8
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework.authtoken import views

from msg.views_api import AlertView
from reports.views_api import DataView

urlpatterns = [
    url(r'^auth/', views.obtain_auth_token),
    url(r'^data/', DataView.as_view()),
    url(r'^alert/', AlertView.as_view()),
    url(r'^msg/', include('msg.urls_api'), name='msg'),
    url(r'^patients/', include('patients.urls_api'), name='patients'),
]
