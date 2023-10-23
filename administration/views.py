from django.conf import settings
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.formats import date_format
from django.utils.http import urlsafe_base64_encode

from administration.forms import ApplicationForm, TransferForm
from administration.models import Application
from administration.serializers import get_applications_serialized_data
from core.utilities import get_date_time_now, send_email
from structure.models import Campus, Residence, Room, Personnel


# Create your views here.
def application(request, template_name="administration/application.html"):

    first_campus = Campus.objects.all().first()
    print(first_campus.name)
    first_campus_res = Residence.objects.filter(campus=first_campus).first()
    first_campus_res_room = Room.objects.filter(residence=first_campus_res).first()
    initial_data = {
        "campus": first_campus,
        "residence": first_campus_res,
        "room": first_campus_res_room
    }

    if request.method == "POST":
        form = ApplicationForm(request.POST, initial_data=initial_data)

        if form.is_valid():
            application = form.save(commit=False)
            date = timezone.now().date()
            student_email = request.user
            student = get_object_or_404(Personnel, student_email=student_email)
            application.student = student
            application.status = Application.Status.SUBMITTED
            application.date = date
            application.room = form.cleaned_data["room"]
            application.save()

            messages.success(
                request,
                "Your application has been submitted successfully!"
            )

            return redirect(reverse("core:dashboard"))

        else:
            messages.error(
                request,
                "There was an error while trying to submit your application"
            )
    else:
        form = ApplicationForm(initial_data=initial_data)

    return TemplateResponse(request, template_name, {"form": form})


# Create your views here.
def transfer(request, template_name="administration/transfer.html"):

    first_campus = Campus.objects.all().first()
    print(first_campus.name)
    first_campus_res = Residence.objects.filter(campus=first_campus).first()
    first_campus_res_room = Room.objects.filter(residence=first_campus_res).first()
    initial_data = {
        "campus": first_campus,
        "residence": first_campus_res,
        "room": first_campus_res_room
    }

    application = get_object_or_404(Application, student__student_email=request.user)

    if request.method == "POST":
        form = TransferForm(request.POST, initial_data=initial_data, application=application)

        if form.is_valid():
            transfer = form.save(commit=False)
            date = timezone.now().date()
            student_email = request.user
            student = get_object_or_404(Personnel, student_email=student_email)
            transfer.application = application
            transfer.student = student
            transfer.date = date
            transfer.room = form.cleaned_data["to_room"]
            transfer.save()
            application.room = form.cleaned_data["to_room"]
            application.save()

            messages.success(
                request,
                "Your transfer request has been submitted successfully!"
            )

            return redirect(reverse("core:dashboard"))

        else:
            messages.error(
                request,
                "There was an error while trying to submit your transfer request"
            )
    else:
        form = TransferForm(initial_data=initial_data)

    return TemplateResponse(request, template_name, {"form": form})


# Create your views here.
def terminate(request):
    application = get_object_or_404(Application, student__student_email=request.user, status=Application.Status.APPROVED)
    application.status = Application.Status.TERMINATED
    application.save()

    messages.success(
        request,
        "Your residency has been terminated successfully"
    )


# Create your views here.
def applications_list(request, template_name="administration/applications-list.html"):
    """
    This function returns a list of all Applications loaded into the system.
    """
    json_ = request.GET.get("json", None)
    search_value = request.GET.get("search[value]", None)

    if json_:
        return get_applications_serialized_data(
            request, search_value=search_value
        )

    return TemplateResponse(request, template_name)


def application_view(request, application_pk, template_name="administration/application-view.html"):
    application = Application.objects.get(pk=application_pk)

    template_context = {"application": application}

    return TemplateResponse(request, template_name, template_context)


def application_approve(request, application_pk):
    application = Application.objects.get(pk=application_pk)
    application.status = Application.Status.APPROVED
    application.save()

    # Send an e-mail message to the user account about the
    # successful application.
    now = get_date_time_now()
    timestamp = date_format(now, "DATETIME_FORMAT", use_l10n=False)
    template = "email/application-approved-confirmation.html"
    subject = f"{settings.SITE_TITLE} - Application Approved"
    email_data = {
        "subject": subject,
        "full_name": f"{application.student.user.first_name.title()}",
        "timestamp": f"{timestamp}",
        "application": application
    }
    recipient = application.student.personal_email

    # Sends the login confirmation email to the person.
    send_email(recipient, subject, template, email_data)

    messages.success(
        request,
        "The application has been approved"
    )

    return redirect(reverse("administration:applications_list"))


def application_decline(request, application_pk):
    application = Application.objects.get(pk=application_pk)
    application.status = Application.Status.REJECTED
    application.save()

    return redirect(reverse("administration:applications_list"))


def application_resolve(request, application_pk):
    application = Application.objects.get(pk=application_pk)
    application.resolved = True
    application.save()

