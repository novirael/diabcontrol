from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView

from patients.models import MyPatients


class PatientList(ListView):
    model = MyPatients
    template_name = 'patients/patients_index.html'

    def get_queryset(self):
        queryset = super(PatientList, self).get_queryset()
        return queryset.filter(doctor=self.request.user)


class PatientDetails(TemplateView):
    template_name = 'patients/details.html'
    patient = None

    def dispatch(self, request, *args, **kwargs):
        self.patient = get_object_or_404(
            User,
            pk=self.kwargs['pk'],
            groups__name__exact='Patient',
        )
        return super(PatientDetails, self).dispatch(
            request, *args, **kwargs
        )

    def get_context_data(self, **kwargs):
        context = super(PatientDetails, self).get_context_data(**kwargs)
        context['patient'] = self.patient
        return context
