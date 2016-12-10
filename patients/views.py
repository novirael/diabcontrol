from datetime import date, timedelta
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView

from patients.models import Relationship
from reports.models import ReportData


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
        context['reports'] = patient.report_set.all()
        return context


class PatientDateMixin(object):
    patient = None
    current_date = None

    def dispatch(self, request, *args, **kwargs):
        self.patient = get_object_or_404(
            User,
            pk=kwargs.pop('pk', 0),
            groups__name__exact='Patient',
        )
        try:
            self.current_date = date(
                int(kwargs.pop('year')),
                int(kwargs.pop('month')),
                int(kwargs.pop('day')),
            )
        except ValueError:
            raise Http404
        return super(PatientDateMixin, self).dispatch(request, *args, **kwargs)


class DailyResultsDetails(PatientDateMixin, TemplateView):
    template_name = 'patients/results_daily.html'

    def get_context_data(self, **kwargs):
        context = super(DailyResultsDetails, self).get_context_data(**kwargs)
        context['date'] = self.current_date
        context['patient'] = self.patient

        context.update(self.get_activity_context())
        context.update(self.get_nutrition_context())
        context.update(self.get_glucose_context())

        return context

    def get_activity_context(self):
        steps_data = ReportData.objects.filter(
            type='steps',
            patient_id=self.patient.id,
            datetime__day=self.current_date.day,
            datetime__month=self.current_date.month,
            datetime__year=self.current_date.year,
        )

        climbed_data = ReportData.objects.filter(
            type='flights_climbed',
            patient_id=self.patient.id,
            datetime__day=self.current_date.day,
            datetime__month=self.current_date.month,
            datetime__year=self.current_date.year,
        )

        heartrate_data_act = ReportData.objects.filter(
            type='heart_rate',
            patient_id=self.patient.id,
            datetime__day=self.current_date.day,
            datetime__month=self.current_date.month,
            datetime__year=self.current_date.year,
        )

        heartrate_data_avg = ReportData.objects.filter(
            type='heart_rate',
            patient_id=self.patient.id,
            datetime__month=(self.current_date.replace(day=1) - timedelta(days=1)).month,
        )

        if heartrate_data_avg:
            avg_prev_hr = sum(
                [data.value for data in heartrate_data_avg]
            )/len(heartrate_data_avg)
        else:
            avg_prev_hr = 0

        if heartrate_data_act:
            actual_avg_heartrate = sum(
                [data.value for data in heartrate_data_act]
            )
        else:
            actual_avg_heartrate = 0

        hr_status = 'default'

        if avg_prev_hr * 1.3 >= actual_avg_heartrate \
                or avg_prev_hr * 0.7 <= actual_avg_heartrate:
            hr_status = 'warning'
        if avg_prev_hr * 1.5 >= actual_avg_heartrate \
                or avg_prev_hr * 0.5 <= actual_avg_heartrate:
            hr_status = 'danger'

        return {
            'steps': sum([data.value for data in steps_data]),
            'flights_climbed': sum([data.value for data in climbed_data]),
            'heart_rate': sum([data.value for data in heartrate_data_act]),
            'avg_prev_hr': avg_prev_hr,
            'hr_status': hr_status if avg_prev_hr else 'default'
        }

    def get_nutrition_context(self):
        fat_data = ReportData.objects.filter(
            type='fat',
            patient_id=self.patient.id,
            datetime__day=self.current_date.day,
            datetime__month=self.current_date.month,
            datetime__year=self.current_date.year,
        )

        protein_data = ReportData.objects.filter(
            type='protein',
            patient_id=self.patient.id,
            datetime__day=self.current_date.day,
            datetime__month=self.current_date.month,
            datetime__year=self.current_date.year,
        )

        carb_data = ReportData.objects.filter(
            type='carbohydrates',
            patient_id=self.patient.id,
            datetime__day=self.current_date.day,
            datetime__month=self.current_date.month,
            datetime__year=self.current_date.year,
        )

        return {
            'fat': sum([data.value for data in fat_data]),
            'protein': sum([data.value for data in protein_data]),
            'carbohydrates': sum([data.value for data in carb_data])
            }

    def get_glucose_context(self):
        glucose_data = ReportData.glucose_measurement.filter(
            patient_id=self.patient.id,
            datetime__day=self.current_date.day,
            datetime__month=self.current_date.month,
            datetime__year=self.current_date.year,
        )
        values = [data.value for data in glucose_data]
        min_glucose, max_glucose, avg_glucose = None, None, None

        if values:
            min_glucose = min(values)
            max_glucose = max(values)
            avg_glucose = sum(values) / len(values)

        status = 'default'
        if any(filter(lambda x: x < 60 or x > 139, values)):
            status = 'danger'
        elif any(filter(lambda x: x < 70 or x > 99, values)):
            status = 'warning'

        return {
            'glucose_min': min_glucose,
            'glucose_max': max_glucose,
            'glucose_avg': avg_glucose,
            'status': status
        }


class MonthlyResultsDetails(TemplateView):
    template_name = 'patients/results_daily.html'


class YearlyResultsDetails(TemplateView):
    template_name = 'patients/results_daily.html'
