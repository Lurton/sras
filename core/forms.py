from django import forms
from django.contrib.auth.hashers import check_password

from core.models import USER_MODEL
from students.models import Student


class LoginForm(forms.Form):
    username = forms.EmailField(
        label="Email Address", max_length=254, required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput, max_length=254, required=True
    )
    next = forms.CharField(widget=forms.HiddenInput, required=False)
    recaptcha = forms.CharField(widget=forms.HiddenInput, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({"autofocus": True})
        self.fields["username"].extras = {"input_group": "@"}

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

        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        # Check if this is a valid and active user / profile on the platform.
        try:
            user = USER_MODEL.objects.get(email=username)
            if not user.is_active:
                error_message = "The user account has been disabled on the system."
                self._errors["username"] = self.error_class([error_message])
                return cleaned_data

            # Confirm the passwords match and are valid.
            valid_password = check_password(password, user.password)
            if not valid_password:
                error_message = "The password is incorrect."
                self._errors["password"] = self.error_class([error_message])
                return cleaned_data

            # Update the `username` to match the `auth_user` model username.
            cleaned_data["username"] = user
        except USER_MODEL.DoesNotExist:
            error_message = (
                "The user account (email address) does not exist on the"
                " system."
            )
            self._errors["username"] = self.error_class([error_message])

        return cleaned_data


class RegistrationForm(forms.ModelForm):
    recaptcha = forms.CharField(widget=forms.HiddenInput, required=True)

    class Meta:
        model = Student
        fields = ["first_name", "last_name", "mobile_number", "email_address"]

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

        self.fields["email_address"].extras = {
            "prepended": '<i class="fal fa-at"></i>'
        }

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

        email_address = cleaned_data.get("email_address")

        # Ensure that email addresses are unique across the system and valid.
        formatted_email = email_address.lower()

        # Check for duplication.
        auth_user_email_count = USER_MODEL.objects.filter(
            email=formatted_email
        ).count()
        if auth_user_email_count >= 1:
            error_message = "A profile with this email address already exists on the system."
            self._errors["email_address"] = self.error_class([error_message])

        self.cleaned_data["email_address"] = formatted_email

        # Verify all numbers, to prevent dirty data.
        mobile_number = cleaned_data.get("mobile_number")
        if mobile_number:
            response = lookup_number(mobile_number)
            if not response:
                self._errors["mobile_number"] = self.error_class([
                    mobile_number_error_message
                ])

        return cleaned_data