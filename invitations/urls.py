from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from invitations.views import InvitationIndex, InviteFormView, AcceptFormView

urlpatterns = [
    url('^index/$', login_required(InvitationIndex.as_view()), name='index'),
    url('^invite/$', login_required(InviteFormView.as_view()), name='invite'),
    url('^accept/$', login_required(AcceptFormView.as_view()), name='accept'),
]
