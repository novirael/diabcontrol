import pyotp
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views import generic
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView

from accounts.forms import RegisterForm, AuthenticateForm
from accounts.models import UserProfile


class LoginView(FormView):
    """
    Provides the ability to login as a user with a username and password
    """
    success_url = '/'
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'accounts/login.html'

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to


class RegisterView(generic.FormView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/'

    def form_valid(self, form):
        user = User(
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            username=form.cleaned_data['email'],
            email=form.cleaned_data['email']
        )

        user.set_password(form.cleaned_data['password'])

        user.save()

        debug = 1
        debug += 2

        response = super(RegisterView, self).form_valid(form)

        return response


class AuthenticateUserView(generic.FormView):
    form_class = AuthenticateForm
    template_name = 'accounts/authenticate.html'
    redirect_field_name = REDIRECT_FIELD_NAME

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = self.success_url

        return redirect_to

    def form_valid(self, form):
        main_key = UserProfile.objects.get_auth_key(self.request.user)
        auth_key = form.cleaned_data['authenticate_key']

        totp = pyotp.TOTP(main_key)

        is_valid = totp.verify(auth_key)

        if is_valid:
            self.request.session['is_authenticated'] = True
            return super(AuthenticateUserView, self).form_valid(form)

        form_errors = form._errors.setdefault('authenticate_key', ErrorList())
        form_errors.append("Invalid autnentication code")

        return super(AuthenticateUserView, self).form_invalid(form)
