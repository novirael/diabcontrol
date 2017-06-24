# encoding: utf-8
from __future__ import unicode_literals

from django.conf.urls import url
from django.views.generic import TemplateView

from accounts import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url('^register/$', views.RegisterView.as_view(), name='register'),
    url('^register/success/$',
        TemplateView.as_view(template_name='accounts/register_success.html'),
        name='register_success'),
    url('^login/', views.LoginView.as_view(), name='login'),
    url('^logout/', auth_views.logout, name='logout'),
    url('^authenticate/', views.AuthenticateUserView.as_view(), name='authenticate'),
]
