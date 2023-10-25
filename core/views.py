from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login as login_user, get_user_model, logout as logout_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView
from django.shortcuts import redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.formats import date_format
from django.utils.http import url_has_allowed_host_and_scheme, urlencode, urlsafe_base64_encode

from api_google.views import verify_recaptcha
from core.forms import LoginForm, RegistrationForm, SearchForm, PasswordResetForm, CorePasswordResetSetForm, ProfileForm
from core.models import BaseUserAuthentication, USER_MODEL, BasePhysicalAddress
from core.utilities import get_client_ip, get_date_time_now, send_email
from administration.apps import AdministrationConfig
from administration.models import Personnel, Application


def index(request, template_name="core/index.html"):
    """
    This is the landing welcome page of the system.
    """
    if request.user:
        if request.user.is_authenticated:
            return redirect("core:dashboard")
    return TemplateResponse(request, template_name)


@login_required
def dashboard(request, template_name="core/dashboard.html"):
    """
    This is the dashboard page of the system after a successful authentication
    attempt.
    """

    user = Personnel.objects.get(student_email=request.user)
    application = Application.objects.filter(student=user).exclude(status=Application.Status.TERMINATED)

    template_context = {
        "name": user.get_full_name,
        "application": application
    }

    return TemplateResponse(request, template_name, template_context)


def register(request, template_name="core/register.html"):
    """
    This is the accounts' registration page that displays registration information which
    needs to be captured before the user can access the system. This is for general
    web users, not users that we have created i.e.: non-account users.
    """
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            requesting_ip = get_client_ip(request)

            # Validate the Google reCaptcha token.
            recaptcha = form.cleaned_data["recaptcha"]
            response = verify_recaptcha(recaptcha, requesting_ip)

            new_student = form.save(commit=False)

            if response.get("success"):
                first_name = form.cleaned_data["first_name"]
                last_name = form.cleaned_data["last_name"]
                email_address = form.cleaned_data["student_email"]
                password = form.cleaned_data["password"]

                user_model = get_user_model()
                password = make_password(password)
                user_account = user_model.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    username=email_address,
                    email=email_address,
                    password=password,
                    is_active=True
                )

                new_student.user = user_account
                new_student.personnel_type = Personnel.Type.STUDENT
                new_student.save()

                messages.success(
                    request,
                    "Your account and profile information have been created"
                    " successfully!"
                )

                return redirect("core:index")

            else:
                messages.error(
                    request,
                    "The Google reCaptcha challenge was unsuccessful. Please try again."
                )
        else:
            messages.error(
                request,
                "There was an error while trying to register the account and"
                " profile. Please try again!"
            )
    else:
        form = RegistrationForm()

    return TemplateResponse(request, template_name, {"form": form})


def login(request, template_name="core/login.html"):
    """
    This is the login page of the application. A username and password is
    required to log in successfully.
    """
    # Check where the login is coming from.
    default_redirect_url = reverse("core:dashboard")
    redirect_url = request.GET.get("next", default_redirect_url)

    # A security check to ensure the redirect url is safe.
    safe_redirect_url = url_has_allowed_host_and_scheme(
        redirect_url, settings.ALLOWED_HOSTS, require_https=True
    )
    if not safe_redirect_url:
        redirect_url = default_redirect_url

    if request.user:
        if request.user.is_authenticated:
            return redirect(redirect_url)

    if request.method == "POST":
        form = LoginForm(request.POST, initial={"next": redirect_url})

        if form.is_valid():
            requesting_ip = get_client_ip(request)

            # Validate the Google reCaptcha token.
            recaptcha = form.cleaned_data["recaptcha"]
            response = verify_recaptcha(recaptcha, requesting_ip)

            if response.get("success"):
                # Do the typical Django authentication.
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                user = authenticate(request, username=username, password=password)

                # Login the user profile / account and redirect.
                login_user(request, user)

                messages.success(
                    request,
                    f"You have been successfully logged into {settings.SITE_TITLE}."
                )

                # By default, send the user to the dashboard or the `safe`
                # redirect_url.
                return redirect(redirect_url)

            else:
                messages.error(
                    request,
                    "The Google reCaptcha challenge was unsuccessful. Please try again."
                )
        else:
            messages.error(
                request,
                "An error occurred while trying to authenticate. Please try again."
            )
    else:
        form = LoginForm(initial={"next": redirect_url})

    return TemplateResponse(request, template_name, {"form": form})


def logout(request):
    """
    Logs you out of the system completely by deleting the session cookie etc.
    """
    logout_user(request)
    messages.success(
        request,
        f"You have successfully logged out of {settings.SITE_TITLE}."
    )
    return redirect("core:index")


def password_reset(request, template_name="core/password-reset.html"):
    """
    This is the password reset  page of the application. An email address
    (username) is required to send the email to.
    """
    if request.method == "POST":
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            requesting_ip = get_client_ip(request)

            # Validate the Google reCaptcha token.
            recaptcha = form.cleaned_data["recaptcha"]
            response = verify_recaptcha(recaptcha, requesting_ip)

            if response.get("success"):
                username = form.cleaned_data["username"]
                user = USER_MODEL.objects.get(email=username)

                # Send an e-mail message to the user account about the
                # successful login.
                now = get_date_time_now()
                timestamp = date_format(now, "DATETIME_FORMAT", use_l10n=False)
                template = "email/password-reset-confirmation.html"
                subject = f"{settings.SITE_TITLE} - Password Reset Confirmation"
                email_data = {
                    "subject": subject,
                    "full_name": f"{user.first_name.title()}",
                    "timestamp": f"{timestamp}",
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user)
                }
                recipient = user.email

                # Sends the login confirmation email to the person.
                send_email(recipient, subject, template, email_data)

                messages.success(
                    request,
                    "You have successfully requested a password reset for your"
                    f" user / profile on {settings.SITE_TITLE}. The details have"
                    " been sent to your email address."
                )

                return redirect("core:index")

            else:
                messages.error(
                    request,
                    "The Google reCaptcha challenge was unsuccessful. Please try again."
                )
        else:
            messages.error(
                request,
                "An error occurred while trying to reset your password. Please try again."
            )
    else:
        form = PasswordResetForm()

    return TemplateResponse(request, template_name, {"form": form})


class CorePasswordResetConfirmView(PasswordResetConfirmView):
    """
    The page to display after the user has reset their password in the
    `CorePasswordReset` class above.
    # Part of the Class-based password reset views.
    # - PasswordResetConfirmView checks the link the user clicked and prompts
    for a new password.
    This uses the built-in Django reset password setup, just override the
    templates etc.
    """
    template_name = "core/password-reset-confirm.html"
    form_class = CorePasswordResetSetForm
    success_url = reverse_lazy("core:password_reset_complete")
    title = None


def password_reset_complete(request):
    """
    The page to display after the user has reset their password in the
    `CorePasswordResetConfirmView` class above.
    # Part of the Class-based password reset views.
    # - PasswordResetCompleteView shows a success message for the above.
    This uses the built-in Django reset password setup, just override the
    templates etc.
    """
    messages.success(
        request,
        "Your password authentication details for your user / profile have"
        " been reset successfully."
    )
    return redirect("core:index")


def profile_view(request, profile_pk, template_name="core/person-view.html"):
    person = get_object_or_404(Personnel, pk=profile_pk)
    address = None
    try:
        address = BasePhysicalAddress.objects.get(profile=person)
    except:
        pass

    template_context = {
        "person": person,
        "address": address
    }

    return TemplateResponse(request, template_name, template_context)


@login_required
def profile_edit(request, profile_pk, template_name="core/profile-edit.html"):
    """
    This is the profile edit page that returns a template that displays a form
    for the editing of a particular person's information on the system.
    """
    profile = get_object_or_404(Personnel, pk=profile_pk)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()

            messages.success(
                request, "The profile has been edited successfully."
            )

            return redirect(profile)

        else:
            messages.error(
                request, "There was an error while trying to edit the profile."
            )

    else:
        form = ProfileForm(instance=profile)

    template_context = {
        "profile": profile,
        "form": form
    }

    return TemplateResponse(request, template_name, template_context)

