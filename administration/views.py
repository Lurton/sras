from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils import timezone

from administration.forms import ApplicationForm, get_residence_choices, get_room_choices
from administration.models import Campus, Residence, Room, Personnel


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
            application.date = date
            application.room = form.cleaned_data["room"]
            application.save()

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


def ajax_residences(request):
    # Base filter response.
    filter_response = {"json_response": True}
    campus_id = request.GET.get("campus_id", None)

    campus = None
    if campus_id:
        campus = Campus.objects.get(pk=campus_id)
    response = get_residence_choices(campus, **filter_response)

    return JsonResponse(response, safe=False)


def ajax_rooms(request):
    # Base filter response.
    filter_response = {"json_response": True}
    residence_id = request.GET.get("residence_id", None)

    residence = None
    if residence_id:
        residence = Residence.objects.get(pk=residence_id)
    response = get_room_choices(residence, **filter_response)

    return JsonResponse(response, safe=False)
