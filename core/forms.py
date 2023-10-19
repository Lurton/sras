from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import password_validators_help_texts
from django.db import models

from core.models import USER_MODEL
from core.utilities import cleanup_string
from administration.models import Personnel


class FormSearchType(models.TextChoices):
    CONTAINS = "contains", "Contains"
    STARTSWITH = "startswith", "Starts With"


class FormSearchStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    ALL = "all", "All"


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
            cleaned_data["username"] = username
            cleaned_data["password"] = password
        except USER_MODEL.DoesNotExist:
            error_message = (
                "The user account (email address) does not exist on the"
                " system."
            )
            self._errors["username"] = self.error_class([error_message])

        return cleaned_data


class RegistrationForm(forms.ModelForm):
    recaptcha = forms.CharField(widget=forms.HiddenInput, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password_repeat = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Personnel
        fields = ["first_name", "last_name", "mobile_number", "student_email", "personal_email", "password", "password_repeat"]

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

        self.fields["personal_email"].extras = {
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


class SearchForm(forms.Form):
    search_type = forms.ChoiceField(
        choices=FormSearchType.choices,
        widget=forms.RadioSelect(), required=True
    )
    search_status = forms.ChoiceField(
        choices=FormSearchStatus.choices,
        widget=forms.RadioSelect(), required=False
    )
    search_parameters = forms.CharField(max_length=64, required=False)

    def __init__(self, *args, **kwargs):
        display_status = kwargs.pop("display_status", True)
        super().__init__(*args, **kwargs)

        self.fields["search_parameters"].widget.attrs.update({"autofocus": True})
        self.fields["search_parameters"].widget.input_type = "search"
        self.fields["search_type"].initial = "contains"
        self.fields["search_type"].widget.attrs.update({
            "class": "custom-control-input"
        })

        if display_status:
            self.fields["search_status"].initial = "active"
            self.fields["search_status"].required = True
            self.fields["search_status"].widget.attrs.update({
                "class": "custom-control-input"
            })
        else:
            self.fields.pop("search_status")


class PasswordResetForm(forms.Form):
    username = forms.EmailField(
        label="Personal Email Address", max_length=254, required=True
    )
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

        # Check if this is a valid and active user / profile on the platform.
        try:
            user = USER_MODEL.objects.get(email=username)
            if not user.is_active:
                error_message = "The user account has been disabled on the system."
                self._errors["username"] = self.error_class([error_message])
        except USER_MODEL.DoesNotExist:
            error_message = (
                "The user account (email address) does not exist on the"
                " system."
            )
            self._errors["username"] = self.error_class([error_message])

        return cleaned_data


class CorePasswordResetSetForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        validation_help_text = password_validators_help_texts()
        help_text = "<br>&nbsp;&nbsp;".join(validation_help_text)

        self.fields["new_password1"].widget.attrs.update({"autofocus": True})
        self.fields["new_password1"].label = "New Password"
        self.fields["new_password1"].help_text = help_text
        self.fields["new_password2"].label = "New Password Confirmation"


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Personnel
        fields = [
            "first_name", "last_name", "birth_date", "mobile_number", "home_number"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.profile = None
        try:
            self.profile = kwargs["instance"]
        except KeyError:
            pass

        self.fields["mobile_number"].extras = {"hr_below": True}
        self.fields["birth_date"].extras = {
            "input_group": "<i class='fal fa-calendar-alt'></i>",
            "hr_above": True
        }
        self.fields["birth_date"].widget.attrs.update({"class": "date-picker"})

    def clean(self):
        cleaned_data = super().clean()

        # This is to catch and display any individual field errors from the form
        # during the default clean.
        if self._errors:
            return cleaned_data

        # Ensure that fields across the system are neat and valid.
        for field, value in cleaned_data.items():
            if isinstance(value, str):
                cleaned_data[field] = value.strip()

        return cleaned_data
