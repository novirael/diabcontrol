# Create your views here.
from django.views.generic import ListView

from msg.models import Message
from patients.models import Relationship


class MessagesGroupsView(ListView):
    template_name = 'messages/list.html'

    def get_queryset(self):
        is_doctor = self.request.user.groups.filter(name='Doctor').exists()

        if is_doctor:
            qs = Relationship.objects.filter(
                doctor=self.request.user
            )

        else:
            qs = Relationship.objects.filter(
                patient=self.request.user
            )

        return qs


class DetailsView(ListView):
    template_name = 'messages/details.html'

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        is_doctor = self.request.user.groups.filter(name='Doctor').exists()

        if is_doctor:
            qs = Message.objects.filter(
                doctor_id=user_id
            )

        else:
            qs = Message.objects.filter(
                patient_id=user_id
            )

        qs = qs.order_by('datetime')

        return qs
