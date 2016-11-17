from django.views.generic import ListView

from patients.models import MyPatients


class PatientList(ListView):
    model = MyPatients
    template_name = 'patients/patients_index.html'

    def get_queryset(self):
        queryset = super(PatientList, self).get_queryset()
        return queryset.filter(doctor=self.request.user)
