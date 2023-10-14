from django import forms

from administration.models import Application, Transfer
from core.utilities import cleanup_string
from structure.forms import get_campus_choices, get_residence_choices, get_room_choices
from structure.models import Residence, Room, Campus


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
            return cleaned_data

        # Ensure that fields across the system are neat and valid.
        for field, value in cleaned_data.items():
            if isinstance(value, str):
                cleaned_data[field] = cleanup_string(value)

        return cleaned_data


class TransferForm(forms.ModelForm):
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
    to_room = forms.ModelChoiceField(
        label="Room",
        required=True,
        queryset=Room.objects.none()
    )

    class Meta:
        model = Transfer
        fields = ["campus", "residence", "to_room"]

    def __init__(self, *args, **kwargs):
        initial_data = kwargs.pop("initial_data", None)
        self.application = kwargs.pop("application", None)
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

        self.fields["to_room"].choices = get_room_choices(initial_res)
        self.fields["to_room"].initial = initial_room

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
                self.fields["to_room"].queryset = room
                self.fields["to_room"].choices = get_room_choices(residence=residence)
                self.fields["to_room"].initial = room.first()
            except (ValueError, TypeError):
                # If there is invalid input ignore.
                pass

        self.fields["campus"].widget.attrs.update({
            "class": "select2",
            "data-placeholder": "Select the campus to move to..."
        })

        self.fields["residence"].widget.attrs.update({
            "class": "select2",
            "data-placeholder": "Select the residence to move to..."
        })

        self.fields["to_room"].widget.attrs.update({
            "class": "select2",
            "data-placeholder": "Select the room to move to..."
        })

    def clean(self):
        cleaned_data = super().clean()

        self.instance.from_room = self.application.room

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
