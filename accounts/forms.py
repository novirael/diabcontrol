# encoding: utf-8
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    YEAR_CHOICES = list(zip(range(1920, 2018), range(1920, 2018)))
    MONTH_CHOICES = list(zip(range(1, 13), range(1, 13)))
    DAY_CHOICES = list(zip(range(1, 32), range(1, 32)))

    CHRONIC_DISEASES_CHOICES = (
        ("hypertension", "Hypertension (high blood pressure)"),
        ("high_cholesterol", "High cholesterol"),
        ("arthritis", "Arthritis"),
        ("ischemic_hear_disease", "Ischemic heart disease (or coronary heart disease)"),
        ("diabetes", "Diabetes"),
        ("CKD", "Chronic kidney disease (CKD)"),
        ("heart_failure", "Heart failure"),
        ("depression", "Depression"),
        ("alzheimer", "Alzheimer’s disease and dementia"),
        ("COPD", "Chronic obstructive pulmonary disease (COPD)"),
    )

    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=GENDER_CHOICES)
    birth_year = forms.ChoiceField(choices=YEAR_CHOICES)
    birth_month = forms.ChoiceField(choices=MONTH_CHOICES)
    birth_day = forms.ChoiceField(choices=DAY_CHOICES)

    chronic_deseassed = forms.ChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=CHRONIC_DISEASES_CHOICES,
        required=False
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }


class AuthenticateForm(forms.Form):
    authenticate_key = forms.CharField(required=True)
