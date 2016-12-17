import pyotp
from django.forms.utils import ErrorList
from django.urls import reverse
from django.utils.functional import cached_property
from django.views import generic

from accounts.forms import AuthenticateForm
from accounts.models import UserProfile
from reports.models import Report


class ReportDetailsView(generic.TemplateView):
    template_name = 'reports/details.html'

    def get_context_data(self, **kwargs):
        kwargs = super(ReportDetailsView, self).get_context_data(**kwargs)

        kwargs['report'] = Report.objects.get(pk=self.kwargs['report_id'])

        return kwargs


class ReportSignView(generic.FormView):
    form_class = AuthenticateForm
    template_name = 'reports/verify.html'

    @cached_property
    def _report(self):
        report = Report.objects.get(pk=self.kwargs['report_id'])
        return report

    def get_success_url(self):
        return reverse('patients:details', args=(self._report.patient_id,))

    def get_context_data(self, **kwargs):
        kwargs = super(ReportSignView, self).get_context_data(**kwargs)
        kwargs['report'] = self._report

        return kwargs

    def form_valid(self, form):
        main_key = UserProfile.objects.get_auth_key(self.request.user)
        auth_key = form.cleaned_data['authenticate_key']

        totp = pyotp.TOTP(main_key)

        is_valid = totp.verify(auth_key)

        if is_valid:
            report = self._report
            report.verified_by = self.request.user
            report.save()
            return super(ReportSignView, self).form_valid(form)

        form_errors = form._errors.setdefault('authenticate_key', ErrorList())
        form_errors.append("Invalid verification code")

        return super(ReportSignView, self).form_invalid(form)
