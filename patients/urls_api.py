from django.conf.urls import url

from patients.views_api import RelationshipListView

urlpatterns = [
    url('^/relations$', RelationshipListView.as_view(), name='relations'),
]
