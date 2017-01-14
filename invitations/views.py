from django import forms
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from invitations.models import Invitation
from patients.models import Relationship


class InvitationIndex(ListView):
    template_name = 'invitations/index.html'
    model = Invitation


class InviteForm(forms.Form):
    doctor = forms.ChoiceField(required=True)


class InviteFormView(FormView):
    form_class = InviteForm
    template_name = 'invitations/invite.html'
    success_url = reverse_lazy("invitations:index")

    def get_form(self, form_class=None):
        form = super(InviteFormView, self).get_form(form_class)

        all_doctors = User.objects.filter(groups__name__exact='Doctor')
        all_doctors_ids = set([d.id for d in all_doctors])

        my_current_inv = Invitation.objects.filter(patient=self.request.user)
        my_current_inv = set([i.doctor.id for i in my_current_inv])

        my_doctors_relations = Relationship.objects.filter(patient=self.request.user)
        my_doctors_ids = set([r.doctor.id for r in my_doctors_relations])

        av_doctors_its = all_doctors_ids - my_doctors_ids - my_current_inv

        available_doctors = User.objects.filter(
            id__in=av_doctors_its
        )

        form.fields['doctor'].choices = (
            (doctor.id, doctor.get_full_name())
            for doctor in available_doctors
        )

        return form

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
        Relationship.objects.create(
            doctor=invitation.doctor,
            patient=invitation.patient
        )
        return super(AcceptFormView, self).form_valid(form)
