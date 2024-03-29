import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from structure.forms import get_residence_choices, get_room_choices, RoomEditForm, CampusEditForm, ResidenceEditForm, \
    CampusAddForm, ResidenceAddForm, RoomAddForm
from structure.models import Campus, Residence, Room
from structure.serializers import (
    get_campus_serialized_data, get_residences_serialized_data, get_rooms_serialized_data
)


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


def residence_list(request, template_name="structure/residence-list.html"):
    """
    This function returns a list of all Residences loaded into the system.
    """
    json_ = request.GET.get("json", None)
    search_value = request.GET.get("search[value]", None)

    if json_:
        return get_residences_serialized_data(
            request, search_value=search_value
        )

    return TemplateResponse(request, template_name)


def residence_list(request, template_name="structure/room-list.html"):
    """
    This function returns a list of all Rooms loaded into the system.
    """
    json_ = request.GET.get("json", None)
    search_value = request.GET.get("search[value]", None)

    if json_:
        return get_rooms_serialized_data(
            request, search_value=search_value
        )

    return TemplateResponse(request, template_name)


# Create your views here.
def campus_view(request, campus_pk, template_name="structure/campus-view.html"):
    """
    This function returns a view of all Campuses loaded into the system.
    """
    campus = get_object_or_404(Campus, pk=campus_pk)
    template_context = {
        "campus": campus
    }

    return TemplateResponse(request, template_name, template_context)


# Create your views here.
def campus_edit(request, campus_pk, template_name="structure/campus-edit.html"):
    """
    This function returns a view of all Campuses loaded into the system.
    """
    campus = get_object_or_404(Campus, pk=campus_pk)

    if request.method == "POST":
        form = CampusEditForm(request.POST, instance=campus)

        if form.is_valid():
            updated_campus = form.save()
            messages.success(request, "The room was edited successfully")
            return redirect(updated_campus)
        else:
            messages.error(
                request,
                "There was an error while trying to edit the room."
            )

    else:
        form = CampusEditForm(instance=campus)

    template_context = {
        "form": form,
        "campus": campus
    }

    return TemplateResponse(request, template_name, template_context)


# Create your views here.
def campus_add(request, template_name="structure/campus-add.html"):
    """
    This function returns a view of all Campuses loaded into the system.
    """
    if request.method == "POST":
        form = CampusAddForm(request.POST)

        if form.is_valid():
            updated_campus = form.save()
            messages.success(request, "The campus was added successfully")
            return redirect(updated_campus)
        else:
            messages.error(
                request,
                "There was an error while trying to add the campus."
            )

    else:
        form = CampusAddForm()

    template_context = {
        "form": form
    }

    return TemplateResponse(request, template_name, template_context)


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
def residence_view(request, residence_pk, template_name="structure/residence-view.html"):
    """
    This function returns a view of all Campuses loaded into the system.
    """
    residence = get_object_or_404(Residence, pk=residence_pk)
    template_context = {
        "residence": residence
    }

    return TemplateResponse(request, template_name, template_context)


# Create your views here.
def residence_edit(request, residence_pk, template_name="structure/residence-edit.html"):
    """
    This function returns a view of all Campuses loaded into the system.
    """
    residence = get_object_or_404(Residence, pk=residence_pk)

    if request.method == "POST":
        form = ResidenceEditForm(request.POST, instance=residence)

        if form.is_valid():
            updated_campus = form.save()
            messages.success(request, "The room was edited successfully")
            return redirect(updated_campus)
        else:
            messages.error(
                request,
                "There was an error while trying to edit the room."
            )

    else:
        form = ResidenceEditForm(instance=residence)

    template_context = {
        "form": form,
        "residence": residence
    }

    return TemplateResponse(request, template_name, template_context)


# Create your views here.
def residence_add(request, template_name="structure/residence-add.html"):
    """
    This function returns a view of all Campuses loaded into the system.
    """
    if request.method == "POST":
        form = ResidenceAddForm(request.POST)

        if form.is_valid():
            updated_residence = form.save()
            messages.success(request, "The residence was added successfully")
            return redirect(updated_residence)
        else:
            messages.error(
                request,
                "There was an error while trying to add the residence."
            )

    else:
        form = ResidenceAddForm()

    template_context = {
        "form": form
    }

    return TemplateResponse(request, template_name, template_context)


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


# Create your views here.
def room_view(request, room_pk, template_name="structure/room-view.html"):
    """
    This function returns a view of all Campuses loaded into the system.
    """
    room = get_object_or_404(Room, pk=room_pk)
    template_context = {
        "room": room
    }

    return TemplateResponse(request, template_name, template_context)


# Create your views here.
def room_edit(request, room_pk, template_name="structure/room-edit.html"):
    """
    This function returns a view of all Campuses loaded into the system.
    """
    room = get_object_or_404(Room, pk=room_pk)

    if request.method == "POST":
        form = RoomEditForm(request.POST, instance=room)

        if form.is_valid():
            updated_room = form.save()
            messages.success(request, "The room was edited successfully")
            return redirect(updated_room)
        else:
            messages.error(
                request,
                "There was an error while trying to edit the room."
            )

    else:
        form = RoomEditForm(instance=room)

    template_context = {
        "form": form,
        "room": room
    }

    return TemplateResponse(request, template_name, template_context)


# Create your views here.
def room_add(request, template_name="structure/room-add.html"):
    """
    This function adds a room into the system.
    """
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
        form = RoomAddForm(request.POST, initial_data=initial_data)

        if form.is_valid():
            updated_room = form.save()
            messages.success(request, "The room was added successfully")
            return redirect(updated_room)
        else:
            messages.error(
                request,
                "There was an error while trying to add the room."
            )

    else:
        form = RoomAddForm(initial_data=initial_data)

    template_context = {
        "form": form
    }

    return TemplateResponse(request, template_name, template_context)


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
