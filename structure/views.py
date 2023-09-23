import json

from django.http import JsonResponse
from django.template.response import TemplateResponse

from structure.forms import get_residence_choices, get_room_choices
from structure.models import Campus, Residence
from structure.serializers import get_campus_serialized_data, get_residences_serialized_data, get_rooms_serialized_data


# Create your views here.
def campus_list(request, template_name="structure/campus-list.html"):
    """
    This function returns a list of all Campuses loaded into the system.
    """
    json_ = request.GET.get("json", None)
    search_value = request.GET.get("search[value]", None)

    if json_:
        return get_campus_serialized_data(
            request, search_value=search_value
        )

    return TemplateResponse(request, template_name)


# Create your views here.
def residence_list(request, template_name="structure/residence-list.html"):
    """
    This function returns a list of all Campuses loaded into the system.
    """
    json_ = request.GET.get("json", None)
    search_parameters = request.GET.get("search_parameters", {})
    search_value = request.GET.get("search[value]", None)

    if json_:
        if search_parameters:
            search_parameters = json.loads(search_parameters)
        return get_residences_serialized_data(
            request, search_parameters=search_parameters,
            search_value=search_value
        )

    return TemplateResponse(request, template_name)


# Create your views here.
def room_list(request, template_name="structure/room-list.html"):
    """
    This function returns a list of all Campuses loaded into the system.
    """
    json_ = request.GET.get("json", None)
    search_parameters = request.GET.get("search_parameters", {})
    search_value = request.GET.get("search[value]", None)

    if json_:
        if search_parameters:
            search_parameters = json.loads(search_parameters)
        return get_rooms_serialized_data(
            request, search_parameters=search_parameters,
            search_value=search_value
        )

    return TemplateResponse(request, template_name)


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
