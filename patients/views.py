from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, TemplateView

from patients.models import Relationship


class PatientIndex(ListView):
    model = Relationship
    template_name = 'patients/index.html'

    def get_queryset(self):
        queryset = super(PatientIndex, self).get_queryset()
        return queryset.filter(doctor=self.request.user)


class PatientDetails(TemplateView):
    template_name = 'patients/details.html'
    patient = None

    def dispatch(self, request, *args, **kwargs):
        if self.request.session.get('is_authenticated') is not True:
            url = reverse('accounts:authenticate')

            redirect_url = reverse('patients:details', kwargs={'patient_id': kwargs['patient_id']})

            full_redirect_url = '{base_url}?{redirect_field_name}={redirect_url}'.format(
                base_url=url,
                redirect_field_name=REDIRECT_FIELD_NAME,
                redirect_url=redirect_url
            )

            return redirect(full_redirect_url)

        return super(PatientDetails, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        patient = get_object_or_404(
            User,
            pk=self.kwargs['pk'],
            groups__name__exact='Patient',
        )

        context = super(PatientDetails, self).get_context_data(**kwargs)
        context['patient'] = patient
        return context


class DailyResultsDetails(TemplateView):
    template_name = 'patients/results_daily.html'


class MonthlyResultsDetails(TemplateView):
    template_name = 'patients/results_daily.html'


class YearlyResultsDetails(TemplateView):
    template_name = 'patients/results_daily.html'
