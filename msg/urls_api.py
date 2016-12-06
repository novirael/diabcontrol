from django.conf.urls import url

from msg.views_api import MessagesListView, MessagesNewView, MessagesConversationListView

urlpatterns = [
    url('^/$', MessagesConversationListView.as_view(), name='list'),
    url('^/new$', MessagesNewView.as_view(), name='new'),
    url('^/details/(?P<user_id>\d+)$', MessagesListView.as_view(), name='details')
]
