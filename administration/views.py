from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils import timezone

from administration.forms import ApplicationForm, TransferForm
from administration.models import Application
from administration.serializers import get_applications_serialized_data
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

            redirect(reverse("core:dashboard"))

            messages.success(
                request,
                "Your application has been submitted successfully!"
            )

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

            redirect(reverse("core:dashboard"))

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
def applications_list(request, template_name="structure/applications-list.html"):
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
