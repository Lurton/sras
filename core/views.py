from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.formats import date_format
from django.utils.http import url_has_allowed_host_and_scheme, urlencode, urlsafe_base64_encode

from api_google.views import verify_recaptcha
from core.forms import LoginForm, RegistrationForm, SearchForm, PasswordResetForm, CorePasswordResetSetForm
from core.models import BaseUserAuthentication, USER_MODEL
from core.utilities import get_client_ip, get_date_time_now, send_email
from administration.apps import AdministrationConfig
from administration.models import Personnel


def index(request, template_name="core/index.html"):
    """
    This is the landing welcome page of the system.
    """
    if request.user:
        if request.user.is_authenticated:
            # return redirect("core:dashboard")
            pass
    return TemplateResponse(request, template_name)



@login_required
def dashboard(request, template_name="core/dashboard.html"):
    """
    This is the dashboard page of the system after a successful authentication
    attempt.
    """
    # Handle the search if present from the querystring.
    querystring = request.GET
    search_parameters = querystring.dict()

    if request.method == "POST":
        form = SearchForm(request.POST, initial=search_parameters)

        if form.is_valid():
            # Format the input from the form into a "GET" querystring used for
            # the redirect.
            querystring = urlencode(form.cleaned_data)

            redirect_url = reverse("core:dashboard") + f"?{querystring}"

            return redirect(redirect_url)

        else:
            messages.error(
                request, "There was an error while trying to perform the search."
            )

    else:
        form = SearchForm(initial=search_parameters)

    if search_parameters:
        messages.info(
            request, "You entered the following search criteria."
        )
        messages.info(
            request,
            f"{search_parameters.get('search_type').title()}"
            f" | {search_parameters.get('search_status').title()}",
            extra_tags="Search Type | Search Status"
        )
        if search_parameters.get("search_parameters"):
            messages.info(
                request, search_parameters.get("search_parameters"),
                extra_tags="Search Parameters"
            )

    # Fetch all the respective searches from the individual applications.
    # company_queryset = company_search(
    #     request, search_parameters=search_parameters
    # )
    # company_document_queryset = company_document_search(
    #     request, search_parameters=search_parameters
    # )
    # people_queryset = person_search(
    #     request, search_parameters=search_parameters
    # )
    # people_document_queryset = person_document_search(
    #     request, search_parameters=search_parameters
    # )
    # asset_queryset = asset_search(
    #     request, search_parameters=search_parameters
    # )
    # asset_document_queryset = asset_document_search(
    #     request, search_parameters=search_parameters
    # )
    # bank_account_queryset = bank_account_search(
    #     request, search_parameters=search_parameters
    # )
    # customer_queryset = customer_search(
    #     request, search_parameters=search_parameters
    # )
    # contact_queryset = contact_search(
    #     request, search_parameters=search_parameters
    # )
    # location_queryset = location_search(
    #     request, search_parameters=search_parameters
    # )

    dashboard_values = {
        # "companies": {
        #     "company_count": company_queryset.count(),
        #     "document_count": company_document_queryset.count()
        # },
        # "people": {
        #     "people_count": people_queryset.count(),
        #     "document_count": people_document_queryset.count()
        # },
        # "assets": {
        #     "asset_count": asset_queryset.count(),
        #     "document_count": asset_document_queryset.count()
        # },
        # "bank_account_count": bank_account_queryset.count(),
        # "customers": {
        #     "customer_count": customer_queryset.count(),
        #     "contact_count": contact_queryset.count(),
        #     "location_count": location_queryset.count()
        # }
    }

    template_context = {
        "form": form,
        "dashboard_values": dashboard_values,
        # "search_parameters": urlencode(search_parameters)
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

                # Send a welcome email message to the user.
                subject = f"{settings.SITE_TITLE} | Account Information and Profile Sign-Up"
                template = "email/signup-confirmation.html"
                email_data = {
                    "subject": f"{subject}",
                    "full_name": f"{str(first_name).title()} {str(last_name).title()}",
                    "password": f"{password}"
                }
                recipient = email_address

                # send_email(recipient, subject, template, email_data)

                messages.success(
                    request,
                    "Your account and profile information have been created"
                    " successfully!"
                )
                messages.warning(
                    request,
                    "The authentication details for your login have been emailed"
                    " to you!"
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
    print(safe_redirect_url, "safe_redirect_url")

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
            print(response)

            if response.get("success"):
                # Do the typical Django authentication.
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                user = authenticate(request, username=username, password=password)

                # Login the user profile / account and redirect.
                login(request, user)

                # Security checks on the IP address as we also want to record
                # the login attempt in the `BaseAuthentication` table.
                # Note: session checks also occur in the signals.
                # BaseUserAuthentication.objects.create(
                #     user=user,
                #     ip_address=requesting_ip
                # )

                # Send an e-mail message to the user account about the
                # successful login.
                timestamp = get_date_time_now()

                template = "email/login-confirmation.html"
                subject = f"{settings.SITE_TITLE} - Login Confirmation"
                timestamp = date_format(timestamp, "DATETIME_FORMAT", use_l10n=False)
                email_data = {
                    "subject": subject,
                    "full_name": f"{user.first_name.title()}",
                    "timestamp": f"{timestamp}"
                }
                recipient = user.email

                # Sends the login confirmation email to the person.
                # send_email(recipient, subject, template, email_data)

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

                return redirect("core:core_index")

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
