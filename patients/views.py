from datetime import date
from django.contrib.auth.models import User
from django.http import Http404
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
    patient = None

    def get_context_data(self, **kwargs):
        self.patient = get_object_or_404(
            User,
            pk=self.kwargs['pk'],
            groups__name__exact='Patient',
        )

        try:
            current_date = date(
                int(self.kwargs.get('year')),
                int(self.kwargs.get('month')),
                int(self.kwargs.get('day')),
            )
        except ValueError:
            raise Http404

        context = super(DailyResultsDetails, self).get_context_data(**kwargs)
        context['date'] = current_date
        context['patient'] = self.patient

        context.update(self.get_activity_context())
        context.update(self.get_nutrition_context())
        context.update(self.get_glucose_context())

        return context

    def get_activity_context(self):
        return {}

    def get_nutrition_context(self):
        return {}

    def get_glucose_context(self):
        return {}


class MonthlyResultsDetails(TemplateView):
    template_name = 'patients/results_daily.html'


class YearlyResultsDetails(TemplateView):
    template_name = 'patients/results_daily.html'
