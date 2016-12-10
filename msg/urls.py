from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from msg.views import MessagesGroupsView, DetailsView

urlpatterns = [
    url('^$', login_required(MessagesGroupsView.as_view()), name='list'),
    url('^details/(?P<user_id>\d+)', login_required(DetailsView.as_view()), name='details')
]
