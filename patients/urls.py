from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from patients.views import PatientIndex, PatientDetails

urlpatterns = [
    url('^index/$', login_required(PatientIndex.as_view()), name='index'),
    url('^details/(?P<pk>\d+)/$', login_required(PatientDetails.as_view()), name='details'),
]
