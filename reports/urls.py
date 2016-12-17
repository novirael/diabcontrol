from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from reports.views import ReportSignView

urlpatterns = [
    url('^verify/(?P<report_id>[^/]+)/$', login_required(ReportSignView.as_view()), name='verify'),
]
