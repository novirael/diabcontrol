from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from patients.views import PatientList, PatientDetails

urlpatterns = [
    url(r'^$', login_required(PatientList.as_view()), name='list'),
    url(r'^details/(?P<pk>\d+)/$', login_required(PatientDetails.as_view()), name='details'),
]
