from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^patients/', include('patients.urls', namespace='patients')),
    url(r'^invitations/', include('invitations.urls', namespace='invitations')),
    url(r'^msg/', include('msg.urls', namespace='msg')),

    url(r'^api/', include('rest_api.urls', namespace='rest_api')),

    url(r'^$', login_required(TemplateView.as_view(template_name='base.html'))),
]
