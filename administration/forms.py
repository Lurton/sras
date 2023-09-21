from itertools import chain

from django import forms

from administration.models import Application, Campus, Residence, Room
from core.utilities import cleanup_string


def get_campus_choices(json_response=None):
    if json_response:
        response = {"results": []}
    else:
        response = []

    campus_queryset = Campus.objects.all()
    for campus in campus_queryset:
        if json_response:
            response_object = {
                "id": f"{campus.pk}",
                "text": campus.name
            }
            response["results"].append(response_object)
        else:
            response.append((campus.pk, campus.name))

    return response


def get_residence_choices(campus, json_response=None):
    if json_response:
        response = {"results": []}
    else:
        response = []

    residence_queryset = Residence.objects.filter(campus=campus)
    for residence in residence_queryset:
        if json_response:
            response_object = {
                "id": f"{residence.pk}",
                "text": residence.name
            }
            response["results"].append(response_object)
        else:
            response.append((residence.pk, residence.name))
    return response


def get_room_choices(residence, json_response=None):
    if json_response:
        response = {"results": []}
    else:
        response = []

    room_queryset = Room.objects.filter(residence=residence)
    for room in room_queryset:
        if json_response:
            response_object = {
                "id": f"{room.pk}",
                "text": room.number
            }
            response["results"].append(response_object)
        else:
            response.append((room.pk, room.number))
    return response


class ApplicationForm(forms.ModelForm):
    campus = forms.ChoiceField(
        label="Campus",
        required=True,
        widget=forms.Select
    )
    residence = forms.ModelChoiceField(
        label="Residence",
        required=True,
        queryset=Residence.objects.none()
    )
    room = forms.ModelChoiceField(
        label="Room",
        required=True,
        queryset=Room.objects.none()
    )

    class Meta:
        model = Application
        fields = ["campus", "residence", "room"]

    def __init__(self, *args, **kwargs):
        initial_data = kwargs.pop("initial_data", None)
        super().__init__(*args, **kwargs)

        print(initial_data, "FORM")
        print("IN THE FORM")

        initial_campus = initial_data.get("campus")
        initial_res = initial_data.get("residence")
        initial_room = initial_data.get("room")

        self.fields["campus"].choices = get_campus_choices()
        self.fields["campus"].initial = initial_campus

        self.fields["residence"].choices = get_residence_choices(initial_campus)
        self.fields["residence"].initial = initial_res

        self.fields["room"].choices = get_room_choices(initial_res)
        self.fields["room"].initial = initial_room

        if "campus" in self.data:
            try:
                campus_pk = int(self.data.get("campus"))
                campus = Campus.objects.get(pk=campus_pk)
                residence = Residence.objects.filter(campus__pk=campus_pk)
                self.fields["residence"].queryset = residence
                self.fields["residence"].choices = get_residence_choices(campus=campus)
                self.fields["residence"].initial = residence.first()
            except (ValueError, TypeError):
                # If there is invalid input ignore.
                pass

        if "residence" in self.data:
            try:
                residence_pk = int(self.data.get("residence"))
                residence = Residence.objects.get(pk=residence_pk)
                room = Room.objects.filter(residence__pk=residence_pk)
                self.fields["room"].queryset = room
                self.fields["room"].choices = get_room_choices(residence=residence)
                self.fields["room"].initial = room.first()
            except (ValueError, TypeError):
                # If there is invalid input ignore.
                pass

        self.fields["campus"].widget.attrs.update({
            "class": "select2",
            "data-placeholder": "Select the campus..."
        })

        self.fields["residence"].widget.attrs.update({
            "class": "select2",
            "data-placeholder": "Select the residence..."
        })

        self.fields["room"].widget.attrs.update({
            "class": "select2",
            "data-placeholder": "Select the room..."
        })

    def clean(self):
        cleaned_data = super().clean()

        # This is to catch and display any individual field errors from the
        # form during the default clean.
        if self._errors:
            print(self.data["campus"])
            print(self.data["residence"])
            print(self.data["room"])
            print(self._errors)
            return cleaned_data

        # Ensure that fields across the system are neat and valid.
        for field, value in cleaned_data.items():
            if isinstance(value, str):
                cleaned_data[field] = cleanup_string(value)

        return cleaned_data
