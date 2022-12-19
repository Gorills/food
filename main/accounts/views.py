# account/views.py
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from allauth.account.forms import SignupForm
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from allauth.account.views import SignupView, _ajax_response
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.http import (
    Http404,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)

from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateResponseMixin, TemplateView, View
from django.views.generic.edit import FormView

from allauth.exceptions import ImmediateHttpResponse
from allauth.utils import get_form_class, get_request_param
from allauth.account import app_settings, signals
from allauth.account.adapter import get_adapter

from .forms import (
    AddEmailForm,
    ChangePasswordForm,
    LoginForm,
    ResetPasswordForm,
    ResetPasswordKeyForm,
    SetPasswordForm,
    SignupForm,
    UserTokenForm,
    ProfileForm
)
from allauth.account.models import EmailAddress, EmailConfirmation, EmailConfirmationHMAC
from allauth.account.utils import (
    complete_signup,
    get_login_redirect_url,
    get_next_redirect_url,
    logout_on_password_change,
    passthrough_next_redirect_url,
    perform_login,
    sync_user_email_addresses,
    url_str_to_user_pk,
)

from allauth.account.views import RedirectAuthenticatedUserMixin, AjaxCapableProcessFormViewMixin, CloseableSignupMixin

INTERNAL_RESET_URL_KEY = "set-password"
INTERNAL_RESET_SESSION_KEY = "_password_reset_key"


sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters("oldpassword", "password", "password1", "password2")
)

from setup.models import ThemeSettings
try:
    theme_address = ThemeSettings.objects.get().name
except:
    theme_address = 'default'



class SignUpView(generic.CreateView):
    
    template_name = 'account/signup.html'
    

class Login(LoginView):
    template_name = 'account/login.html'


class Logout(LogoutView):
    template_name = 'account/logged_out.html'


# Предварительная регистрация по телефону
from django.views.decorators.http import require_POST
@require_POST
def usersession_add(request):
    if request.session['code']:
        user_phone = request.POST['phone']
        code = request.POST['code']
        if request.session['code'] == code and request.session['phone'] == user_phone:
            try:
                userprofile = UserProfile.objects.get(phone=user_phone)
            except:
                userprofile = UserProfile(phone=user_phone)
                userprofile.save()

            request.session['user_profile_id'] = userprofile.id
            del request.session['code']
            del request.session['code_date']
            del request.session['phone']
            return redirect('home')


       
text = 'Код доступа'


import requests
from datetime import datetime
import random
def generate_code():
    random.seed()
    return str(random.randint(10000,99999))


from sms.views import send_sms

@require_POST
def add_code(request):
    gen_code = True
    session = request.session
    
    session['phone'] = request.POST['phone']

    phone = request.POST['phone']
    
    if 'code' in session and 'code_date' in session:
        if int((datetime.now() - datetime.strptime(request.session["code_date"], '%Y-%m-%d %H:%M:%S.%f')).total_seconds())< 120:
            code = session['code']
            gen_code=False
            
        else:
            del request.session['code']
            gen_code=True
           

    if gen_code:
        request.session["code_date"] = str(datetime.now())
        code = generate_code()
        request.session['code'] = code

        text = 'Ваш код: ' + code
        send_sms(text, phone)
        # print(request.session['code'])
        
        return redirect('home')


    else: 
        return redirect('home')
    

    

from .forms import ProfileForm
from setup.models import BaseSettings

def profile(request):

    try:
        user_profile = UserProfile.objects.get(id=request.session['user_profile_id'])
    except:
        user_profile = None

    

    if user_profile and BaseSettings.objects.get().sms == True:
        default_data = {
            'phone': user_profile.phone, 
        }
        profile_form = ProfileForm(default_data)
        context = {
            # 'user': user, 
            'profile_form': profile_form,
        }
        return render(request, 'global/profile.html', context)
    else:

        return redirect('home')


def profile_orders(request):

    
    try:
        user_profile = UserProfile.objects.get(id=request.session['user_profile_id'])
    except:
        user_profile = None

    if user_profile:
        
        context = {
            'user_profile': user_profile
        }
        return render(request, 'global/profile_orders.html', context)
    else:
        return redirect('home')

@login_required
def profile_wishlist(request):
    
    return render(request, 'global/profile_wishlist.html')


@login_required
def profile_history(request):
    

    context = {

    }

    return render(request, 'global/profile_history.html', context)



@login_required
def profile_update(request):
    
    context = {

    }

    return render(request, 'global/profile_update.html', context)






class LoginView(RedirectAuthenticatedUserMixin, AjaxCapableProcessFormViewMixin, FormView):
    form_class = LoginForm
    # template_name = "account/login." + app_settings.TEMPLATE_EXTENSION
    template_name = 'account/login.html'
    success_url = None
    redirect_field_name = "next"

    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_form_class(self):
        return get_form_class(app_settings.FORMS, "login", self.form_class)

    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            return form.login(self.request, redirect_url=success_url)
        except ImmediateHttpResponse as e:
            return e.response

    def get_success_url(self):
        # Explicitly passed ?next= URL takes precedence
        ret = (
            get_next_redirect_url(self.request, self.redirect_field_name)
            or self.success_url
        )
        return ret

    def get_context_data(self, **kwargs):
        ret = super(LoginView, self).get_context_data(**kwargs)
        signup_url = passthrough_next_redirect_url(
            self.request, reverse("account_signup"), self.redirect_field_name
        )
        redirect_field_value = get_request_param(self.request, self.redirect_field_name)
        site = get_current_site(self.request)

        ret.update(
            {
                "signup_url": signup_url,
                "site": site,
                "redirect_field_name": self.redirect_field_name,
                "redirect_field_value": redirect_field_value,
            }
        )
        return ret


login = LoginView.as_view()





class SignupView(
    RedirectAuthenticatedUserMixin,
    CloseableSignupMixin,
    AjaxCapableProcessFormViewMixin,
    FormView,
    ):
    template_name = 'account/signup.html'
    form_class = SignupForm
    redirect_field_name = "next"
    success_url = None

    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):
        return super(SignupView, self).dispatch(request, *args, **kwargs)

    def get_form_class(self):
        return get_form_class(app_settings.FORMS, "signup", self.form_class)

    def get_success_url(self):
        # Explicitly passed ?next= URL takes precedence
        ret = (
            get_next_redirect_url(self.request, self.redirect_field_name)
            or self.success_url
        )
        return ret

    def form_valid(self, form):
        # By assigning the User to a property on the view, we allow subclasses
        # of SignupView to access the newly created User instance
        self.user = form.save(self.request)
        try:
            return complete_signup(
                self.request,
                self.user,
                app_settings.EMAIL_VERIFICATION,
                self.get_success_url(),
            )
        except ImmediateHttpResponse as e:
            return e.response

    def get_context_data(self, **kwargs):
        ret = super(SignupView, self).get_context_data(**kwargs)
        form = ret["form"]
        email = self.request.session.get("account_verified_email")
        if email:
            email_keys = ["email"]
            if app_settings.SIGNUP_EMAIL_ENTER_TWICE:
                email_keys.append("email2")
            for email_key in email_keys:
                form.fields[email_key].initial = email
        login_url = passthrough_next_redirect_url(
            self.request, reverse("account_login"), self.redirect_field_name
        )
        redirect_field_name = self.redirect_field_name
        site = get_current_site(self.request)
        redirect_field_value = get_request_param(self.request, redirect_field_name)
        ret.update(
            {
                "login_url": login_url,
                "redirect_field_name": redirect_field_name,
                "redirect_field_value": redirect_field_value,
                "site": site,
            }
        )
        return ret


signup = SignupView.as_view()