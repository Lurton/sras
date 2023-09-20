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
    residence = forms.ChoiceField(
        label="Residence",
        required=True,
        widget=forms.Select
    )
    room = forms.ChoiceField(
        label="Room",
        required=True,
        widget=forms.Select
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

        self.fields["campus"].choices = list(chain(
            get_campus_choices(),
        ))

        self.fields["residence"].choices = list(chain(
            get_residence_choices(initial_campus)
        ))

        self.fields["room"].choices = list(chain(
            get_room_choices(initial_res)
        ))

        self.fields["campus"].widget.attrs.update({
            "class": "select2",
            "data-placeholder": "Select the campus..."
        })

        self.fields["residence"].widget.attrs.update({
            "class": "select2",
            "data-placeholder": "Select the residence..."
        })

    def clean(self):
        cleaned_data = super().clean()

        # This is to catch and display any individual field errors from the
        # form during the default clean.
        if self._errors:
            print(self._errors)
            return cleaned_data

        # Ensure that fields across the system are neat and valid.
        for field, value in cleaned_data.items():
            if isinstance(value, str):
                cleaned_data[field] = cleanup_string(value)

        return cleaned_data
