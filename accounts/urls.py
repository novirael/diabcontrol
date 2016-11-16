# encoding: utf-8
from __future__ import unicode_literals

from django.conf.urls import url

from accounts import views

urlpatterns = [
    url('^register/', views.RegisterView.as_view(), name='register'),
    url('^login/', views.LoginView.as_view(), name='login'),
]
