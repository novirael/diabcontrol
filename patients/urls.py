from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from patients.views import PatientList

urlpatterns = [
    url('^$', login_required(PatientList.as_view()), name='list'),
]
