from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from reports.views import ReportSignView, ReportDetailsView

urlpatterns = [
    url('^verify/(?P<report_id>[^/]+)/$', login_required(ReportSignView.as_view()), name='verify'),
    url('^details/(?P<report_id>[^/]+)/$', login_required(ReportDetailsView.as_view()), name='details'),
]
