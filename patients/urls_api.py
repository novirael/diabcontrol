from django.conf.urls import url

from patients.charts import DailyGlucoseLevelJSONView
from patients.views_api import RelationshipListView

urlpatterns = [
    url('^relations$', RelationshipListView.as_view(), name='relations'),
    url('^(?P<pk>\d+)/charts/glucose/daily/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d+)/$',
        DailyGlucoseLevelJSONView.as_view(), name='daily_glucose_chart')
]
