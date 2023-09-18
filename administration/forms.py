from itertools import chain

from django import forms

from administration.models import Application, Campus, Residence, Room
from core.utilities import cleanup_string


def get_campus_choices():
    queryset = Campus.objects.all()
    return queryset.values_list("pk", "name")

def get_residence_choices(campus):
    queryset = Residence.objects.filter(campus=campus)
    return queryset.values_list("pk", "name")

def get_room_choices(residence):
    queryset = Room.objects.filter(residence=residence)
    return queryset.values_list("pk", "number")


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
