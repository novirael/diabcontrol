from django.conf.urls import url

from patients.charts import (
    DailyGlucoseLevelJSONView,
    MonthlyGlucoseLevelJSONView,
    YearlyGlucoseLevelJSONView,
)
from patients.views_api import RelationshipListView

urlpatterns = [
    url('^relations$', RelationshipListView.as_view(), name='relations'),
    url('^(?P<pk>\d+)/charts/glucose/daily/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d+)/$',
        DailyGlucoseLevelJSONView.as_view(), name='daily_glucose_chart'),
    url('^(?P<pk>\d+)/charts/glucose/monthly/(?P<year>\d{4})/(?P<month>\d{2})/$',
        MonthlyGlucoseLevelJSONView.as_view(), name='monthly_glucose_chart'),
    url('^(?P<pk>\d+)/charts/glucose/yearly/(?P<year>\d{4})/$',
        YearlyGlucoseLevelJSONView.as_view(), name='yearly_glucose_chart'),
]
