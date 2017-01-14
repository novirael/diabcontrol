from django.conf.urls import url

from patients.charts import (
    DailyGlucoseLevelJSONView,
    MonthlyGlucoseLevelJSONView,
    YearlyGlucoseLevelJSONView,
    DailyHrLevelJSONView, DailyMacrosLevelJSONView, DailyStepsLevelJSONView, MonthlyHrLevelJSONView,
    MonthlyStepsLevelJSONView, MonthlyClimbedLevelJSONView, MonthlyMacrosLevelJSONView, YearlyHrLevelJSONView,
    YearlyClimbedLevelJSONView, YearlyStepsLevelJSONView, YearlyMacrosLevelJSONView)
from patients.views_api import RelationshipListView

urlpatterns = [
    url('^relations$', RelationshipListView.as_view(), name='relations'),
    url('^(?P<pk>\d+)/charts/glucose/daily/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        DailyGlucoseLevelJSONView.as_view(), name='daily_glucose_chart'),
    url('^(?P<pk>\d+)/charts/glucose/monthly/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        MonthlyGlucoseLevelJSONView.as_view(), name='monthly_glucose_chart'),
    url('^(?P<pk>\d+)/charts/glucose/yearly/(?P<year>\d{4})/$',
        YearlyGlucoseLevelJSONView.as_view(), name='yearly_glucose_chart'),

    url('^(?P<pk>\d+)/charts/hr/daily/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        DailyHrLevelJSONView.as_view(), name='daily_hr_chart'),
    url('^(?P<pk>\d+)/charts/hr/monthly/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        MonthlyHrLevelJSONView.as_view(), name='monthly_hr_chart'),
    url('^(?P<pk>\d+)/charts/hr/yearly/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        YearlyHrLevelJSONView.as_view(), name='yearly_hr_chart'),

    url('^(?P<pk>\d+)/charts/macros/daily/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        DailyMacrosLevelJSONView.as_view(), name='daily_macros_chart'),
    url('^(?P<pk>\d+)/charts/macros/monthly/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        MonthlyMacrosLevelJSONView.as_view(), name='monthly_macros_chart'),
    url('^(?P<pk>\d+)/charts/macros/yearly/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        YearlyMacrosLevelJSONView.as_view(), name='yearly_macros_chart'),

    url('^(?P<pk>\d+)/charts/steps/daily/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        DailyStepsLevelJSONView.as_view(), name='daily_steps_chart'),
    url('^(?P<pk>\d+)/charts/steps/monthly/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        MonthlyStepsLevelJSONView.as_view(), name='monthly_steps_chart'),
    url('^(?P<pk>\d+)/charts/steps/yearly/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        YearlyStepsLevelJSONView.as_view(), name='yearly_steps_chart'),

    url('^(?P<pk>\d+)/charts/climbed/monthly/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        MonthlyClimbedLevelJSONView.as_view(), name='monthly_climbed_chart'),
    url('^(?P<pk>\d+)/charts/climbed/yearly/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        YearlyClimbedLevelJSONView.as_view(), name='yearly_climbed_chart'),
]
