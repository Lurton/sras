from itertools import chain

from django.db.models import BLANK_CHOICE_DASH
from django import forms

from core.utilities import cleanup_string
from structure.models import Campus, Residence, Room


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


def get_residence_choices(campus=None, json_response=None):
    if json_response:
        response = {"results": []}
    else:
        response = []

    if campus:
        residence_queryset = Residence.objects.filter(campus=campus)
    else:
        residence_queryset = Residence.objects.all()

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


class ResidenceAddForm(forms.ModelForm):
    campus = forms.ChoiceField(
        label="Campus",
        required=True,
        widget=forms.Select
    )

    class Meta:
        model = Residence
        fields = ["name", "campus"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["campus"].choices = get_campus_choices()

        self.fields["campus"].widget.attrs.update({
            "class": "select2",
            "data-placeholder": "Select the campus this residence belongs to..."
        })

        self.fields["name"].label = "Residence name"

    def clean(self):
        cleaned_data = super().clean()

        # This is to catch and display any individual field errors from the
        # form during the default clean.
        if self._errors:
            return cleaned_data

        # Ensure that fields across the system are neat and valid.
        for field, value in cleaned_data.items():
            if isinstance(value, str):
                cleaned_data[field] = cleanup_string(value)

        self.cleaned_data["campus"] = Campus.objects.get(pk=self.cleaned_data["campus"])

        return cleaned_data


class ResidenceEditForm(forms.ModelForm):

    class Meta:
        model = Residence
        fields = ["name", "campus", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            residence = kwargs["instance"]
        except KeyError:
            pass

        self.fields["campus"].choices = list(chain(
            get_campus_choices()
        ))

    def clean(self):
        cleaned_data = super().clean()

        # This is to catch and display any individual field errors from the
        # form during the default clean.
        if self._errors:
            return cleaned_data

        # Ensure that fields across the system are neat and valid.
        for field, value in cleaned_data.items():
            if isinstance(value, str):
                cleaned_data[field] = value.strip()

        return cleaned_data


class RoomEditForm(forms.ModelForm):

    class Meta:
        model = Room
        fields = ["number", "floor", "residence", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            room = kwargs["instance"]
        except KeyError:
            pass

        self.fields["residence"].choices = list(chain(
            get_residence_choices()
        ))
        self.fields["number"].label = "Enter the room number"
        self.fields["floor"].label = "Room floor"

    def clean(self):
        cleaned_data = super().clean()

        # This is to catch and display any individual field errors from the
        # form during the default clean.
        if self._errors:
            return cleaned_data

        # Ensure that fields across the system are neat and valid.
        for field, value in cleaned_data.items():
            if isinstance(value, str):
                cleaned_data[field] = value.strip()

        return cleaned_data


class RoomAddForm(forms.ModelForm):
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

    class Meta:
        model = Room
        fields = ["campus", "residence", "number", "floor"]

    def __init__(self, *args, **kwargs):
        initial_data = kwargs.pop("initial_data", None)
        super().__init__(*args, **kwargs)

        initial_campus = initial_data.get("campus")
        initial_res = initial_data.get("residence")

        self.fields["campus"].choices = get_campus_choices()
        self.fields["campus"].initial = initial_campus

        self.fields["residence"].choices = get_residence_choices(initial_campus)
        self.fields["residence"].initial = initial_res

        self.fields["number"].label = "Room number"
        self.fields["floor"].label = "Room floor"

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

        self.fields["campus"].widget.attrs.update({
            "class": "select2",
            "data-placeholder": "Select the campus for the dorm..."
        })

        self.fields["residence"].widget.attrs.update({
            "class": "select2",
            "data-placeholder": "Select the residence for the dorm..."
        })

    def clean(self):
        cleaned_data = super().clean()

        # This is to catch and display any individual field errors from the
        # form during the default clean.
        if self._errors:
            return cleaned_data

        # Ensure that fields across the system are neat and valid.
        for field, value in cleaned_data.items():
            if isinstance(value, str):
                cleaned_data[field] = cleanup_string(value)

        return cleaned_data


class CampusEditForm(forms.ModelForm):
    class Meta:
        model = Campus
        fields = ["name", "location", "address", "email_address", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            campus = kwargs["instance"]
        except KeyError:
            pass

    def clean(self):
        cleaned_data = super().clean()

        # This is to catch and display any individual field errors from the
        # form during the default clean.
        if self._errors:
            return cleaned_data

        # Ensure that fields across the system are neat and valid.
        for field, value in cleaned_data.items():
            if isinstance(value, str):
                cleaned_data[field] = value.strip()

        return cleaned_data


class CampusAddForm(forms.ModelForm):
    class Meta:
        model = Campus
        fields = ["name", "location", "address", "email_address", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].label = "Campus Name"

    def clean(self):
        cleaned_data = super().clean()

        # This is to catch and display any individual field errors from the
        # form during the default clean.
        if self._errors:
            return cleaned_data

        # Ensure that fields across the system are neat and valid.
        for field, value in cleaned_data.items():
            if isinstance(value, str):
                cleaned_data[field] = value.strip()

        return cleaned_data
