from itertools import chain

from django import forms

from administration.models import Application, Campus
from core.utilities import cleanup_string


def get_campus_choices():
    queryset = Campus.objects.all()
    return queryset.values_list("pk", "name")


class ApplicationForm(forms.ModelForm):
    campus = forms.ChoiceField(
        widget=forms.Select,
        choices=get_campus_choices(),
        # initial=REVIEWED_FALSE
    )
    residence = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Application
        fields = ["campus", "residence", "room"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields["campus"].choices = list(chain(
        #     get_campus_choices()
        # ))

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
