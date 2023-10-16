from django.contrib.auth import get_user_model
from django.db import models
from django_countries.fields import CountryField

from django_extensions.db.models import TimeStampedModel
from core.validators import telephone_number_validator

USER_MODEL = get_user_model()


class BaseUserAuthentication(TimeStampedModel):
    user = models.OneToOneField(
        USER_MODEL, null=True, blank=True, on_delete=models.CASCADE
    )
    first_name = models.CharField("First Name", max_length=30)
    last_name = models.CharField("Last Name", max_length=150)
    birth_date = models.DateField(
        "Date of Birth", null=True, blank=True,
        help_text="The date of birth is in the following format e.g.: yyyy-mm-dd."
    )
    mobile_number = models.CharField(
        "Mobile Number", max_length=10, validators=telephone_number_validator
    )
    home_number = models.CharField(
        "Home Number", max_length=10, blank=True,
        validators=telephone_number_validator
    )
    student_email = models.EmailField("Student Email")

    class Meta:
        ordering = ["first_name", "last_name"]
        abstract = True

    @property
    def get_birthday_day(self):
        if self.birth_date:
            return f"{self.birth_date.strftime('%d %B')}"
        return None

    @property
    def get_initials(self):
        initials_list = [str(self.first_name)[0].upper()]
        if self.middle_name:
            initials_list.append(str(self.middle_name)[0].upper())
        return "".join(initials_list)

    @property
    def get_full_name(self):
        return f"{self.first_name.title()} {self.last_name.title()}"

    def __str__(self):
        return self.get_full_name


class AuthenticationAudit(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    person = models.ForeignKey(
        "administration.Personnel",
        null=True,
        blank=True,
        limit_choices_to={"user__is_active": True},
        on_delete=models.CASCADE
    )
    ip_address = models.GenericIPAddressField("IP Address")

    class Meta:
        verbose_name = "Authentication Audit"
        verbose_name_plural = "Authentication Audits"
        ordering = ["timestamp"]
        constraints = [
            models.UniqueConstraint(
                fields=["timestamp", "ip_address"],
                name="authentication_audit_timestamp_ip_address"
            )
        ]

    def __str__(self):
        return f"{self.timestamp} [{self.ip_address}]"


class BasePhysicalAddress(models.Model):
    profile = models.OneToOneField(
        "administration.Personnel",
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    line_1 = models.CharField(
        "Address Line 1",
        max_length=128,
        blank=True
    )
    line_2 = models.CharField(
        "Address Line 2",
        max_length=128,
        blank=True
    )
    line_3 = models.CharField(
        "Address Line 3",
        max_length=128,
        blank=True
    )
    city = models.CharField(
        "City or Town",
        blank=True,
        max_length=64
    )
    country = CountryField()
    code = models.CharField(
        blank=True,
        max_length=12
    )

    class Meta:
        verbose_name = "Physical Address"
        verbose_name_plural = "Physical Addresses"

    @property
    def get_gps_coordinates(self):
        if self.gps_latitude and self.gps_longitude:
            return "{}, {}".format(self.gps_latitude, self.gps_longitude)
        return None

    @property
    def get_full_address(self):
        result = []
        if self.line_1:
            result.append(self.line_1)
        if self.line_2:
            result.append(self.line_2)
        if self.line_3:
            result.append(self.line_3)
        result.append(self.city)
        result.append(self.country.name)
        result.append(self.code)
        return ", ".join(result)

    def __str__(self):
        return "{}".format(self.get_full_address)
