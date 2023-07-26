from django import forms
from django.contrib.auth.hashers import check_password

from core.models import USER_MODEL


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