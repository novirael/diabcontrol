# encoding: utf-8
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']


class AuthenticateForm(forms.Form):
    authenticate_key = forms.CharField(required=True)
