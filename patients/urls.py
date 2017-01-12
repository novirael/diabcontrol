from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from patients.views import PatientIndex, PatientDetails, DailyResultsDetails, MonthlyResultsDetails, \
    YearlyResultsDetails

urlpatterns = [
    url('^index/$', login_required(PatientIndex.as_view()), name='index'),
    url('^details/(?P<pk>\d+)/$', login_required(PatientDetails.as_view()), name='details'),

    url('^details/(?P<pk>\d+)/results/daily/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})$',
        login_required(DailyResultsDetails.as_view()), name='daily_results'),
    url('^details/(?P<pk>\d+)/results/monthly/(?P<year>\d{4})/(?P<month>\d{1,2})$',
        login_required(MonthlyResultsDetails.as_view()), name='monthly_results'),
    url('^details/(?P<pk>\d+)/results/yearly/(?P<year>\d{4})$',
        login_required(YearlyResultsDetails.as_view()), name='yearly_results'),
]
