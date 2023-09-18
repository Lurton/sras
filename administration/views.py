from django.contrib import messages
from django.http import JsonResponse
from django.template.response import TemplateResponse

from administration.forms import ApplicationForm, get_residence_choices, get_room_choices
from administration.models import Campus, Residence


# Create your views here.
def application(request, template_name="administration/application.html"):

    first_campus = Campus.objects.all().first()
    print(first_campus.name)
    first_campus_res = Residence.objects.filter(campus=first_campus).first()
    initial_data = {
        "campus": first_campus,
        "residence": first_campus_res
    }

    if request.method == "POST":
        form = ApplicationForm(request.POST, initial_data=initial_data)

        if form.is_valid():
            print("SUBMITTED SUCCESSFULLY")
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
    campus_id = request.GET.get("campus_id", None)

    if campus_id:
        campus = Campus.objects.get(pk=campus_id)
        response = get_residence_choices(campus=campus)

        return JsonResponse(response, safe=False)


def ajax_rooms(request):
    residence_id = request.GET.get("residence_id", None)

    if residence_id:
        residence = Campus.objects.get(pk=residence_id)
        response = get_room_choices(residence=residence)

        return JsonResponse(response, safe=False)
