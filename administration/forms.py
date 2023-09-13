from django import forms

from administration.models import Application


class ApplicationForm(forms.ModelForm):
    campus = forms.CharField(widget=forms.PasswordInput, required=True)
    residence = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Application
        fields = ["campus", "residence", "room"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["first_name"].widget.attrs.update({"autofocus": True})

        self.fields["last_name"].label = "Last Name"

        self.fields["mobile_number"].widget.input_type = "tel"
        self.fields["mobile_number"].widget.attrs.update({
            "data-toggle": "tooltip", "title": "e.g.: 0821234567"
        })
        self.fields["mobile_number"].extras = {
            "prepended": '<i class="fal fa-mobile"></i>'
        }

        self.fields["student_email"].extras = {
            "prepended": '<i class="fal fa-at"></i>'
        }

        self.fields["password_repeat"].label = "Repeat Password"

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

        email_address = cleaned_data.get("student_email")

        # Ensure that email addresses are unique across the system and valid.
        formatted_email = email_address.lower()

        # Check for duplication.
        auth_user_email_count = USER_MODEL.objects.filter(
            email=formatted_email
        ).count()
        if auth_user_email_count >= 1:
            error_message = "A profile with this email address already exists on the system."
            self._errors["student_email"] = self.error_class([error_message])

        if formatted_email[-13:] != "@mycput.ac.za":
            error_message = "Invalid student email"
            self._errors["student_email"] = self.error_class([error_message])

        if len(formatted_email) != 22:
            error_message = "That student email is incorrect"
            self._errors["student_email"] = self.error_class([error_message])

        self.cleaned_data["student_email"] = formatted_email

        # Verify all numbers, to prevent dirty data.
        mobile_number = cleaned_data.get("mobile_number")
        if mobile_number:
            if len(mobile_number) != 10:
                error_message = "Mobile number must be 10 digits"
                self._errors["mobile_number"] = self.error_class([error_message])

        password = cleaned_data.get("password")
        password_repeat = cleaned_data.get("password_repeat")

        if password != password_repeat:
            error_message = "The 2 passwords do no match"
            self._errors["password_repeat"] = self.error_class([error_message])

        return cleaned_data