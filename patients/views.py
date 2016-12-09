from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
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
