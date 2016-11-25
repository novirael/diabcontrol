from django import forms
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, ListView

from invitations.models import Invitation


class InvitationIndex(ListView):
    template_name = 'invitations/index.html'
    model = Invitation


class InviteForm(forms.Form):
    doctor = forms.ChoiceField(required=True)

    def __init__(self, *args, **kwargs):
        super(InviteForm, self).__init__(*args, **kwargs)
        available_doctors = User.objects.filter(
            groups__name__exact='Doctor',
            doctor_invitations__isnull=True
        )
        self.fields['doctor'].choices = (
            (doctor.id, doctor.get_full_name())
            for doctor in available_doctors
        )


class InviteFormView(FormView):
    form_class = InviteForm
    template_name = 'invitations/invite.html'
    success_url = reverse_lazy("invitations:index")

    def form_valid(self, form):
        Invitation.objects.create(
            doctor_id=form.data['doctor'],
            patient_id=self.request.user.id
        )
        return super(InviteFormView, self).form_valid(form)


class AcceptForm(forms.Form):
    invitation = forms.TextInput()


class AcceptFormView(FormView):
    form_class = AcceptForm
    template_name = 'invitations/index.html'
    success_url = reverse_lazy("invitations:index")

    def form_valid(self, form):
        invitation = Invitation.objects.get(
            pk=form.data['invitation']
        )
        invitation.is_accepted = True
        invitation.save()
        return super(AcceptFormView, self).form_valid(form)
