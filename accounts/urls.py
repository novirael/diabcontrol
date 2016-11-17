# encoding: utf-8
from __future__ import unicode_literals

from django.conf.urls import url

from accounts import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url('^register/', views.RegisterView.as_view(), name='register'),
    url('^login/', views.LoginView.as_view(), name='login'),
    url('^logout/', auth_views.logout, name='logout')
]
