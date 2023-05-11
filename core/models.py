from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator
from django.db import models

from django_extensions.db.models import TimeStampedModel

from core.validators import telephone_number_validator

USER_MODEL = get_user_model()

class BasePhysicalAddress(models.Model):
    class ProvinceChoices(models.IntegerChoices):
        EASTERN_CAPE = 1, "Eastern Cape"
        FREE_STATE = 2, "Free State"
        GAUTENG = 3, "Gauteng"
        KWA_ZULU_NATAL = 4, "Kwazulu Natal"
        LIMPOPO = 5, "Limpopo"
        MPUMALANGA = 6, "Mpumalanga"
        NORTH_WEST = 7, "North West"
        NORTHERN_CAPE = 8, "Northern Cape"
        WESTERN_CAPE = 9, "Western Cape"

    line_1 = models.CharField("Line 1", max_length=128, blank=True)
    line_2 = models.CharField("Line 2", max_length=128, blank=True)
    line_3 = models.CharField("Line 3", max_length=128, blank=True)
    city = models.CharField(max_length=64)
    province = models.PositiveIntegerField(
        choices=ProvinceChoices,
        default=ProvinceChoices.WESTERN_CAPE
    )
    code = models.CharField(max_length=12)
    gps_coordinates = models.CharField(
        "GPS Coordinates", max_length=20, blank=True,
        help_text='The GPS coordinates are in the following format e.g.: "-25.79435, 28.30256".'
    )
    notes = models.TextField(blank=True, validators=[MaxLengthValidator(500)])

    class Meta:
        verbose_name = "Physical Address"
        verbose_name_plural = "Physical Addresses"
        abstract = True

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
        result.append(self.get_province_display())
        result.append(self.code)
        return ", ".join(result)

    def __str__(self):
        return f"{self.get_full_address}"


class BaseUserAuthentication(TimeStampedModel):
    user = models.OneToOneField(
        USER_MODEL, null=True, blank=True, on_delete=models.CASCADE
    )
    code = models.CharField(
        "Person Code", max_length=10, unique=True,
        help_text="This is a unique person code and is in the following format:"
                  " three letters of the object type, followed by a hyphen,"
                  " followed by six digits which increment. e.g.: PER-000001."
                  " This value will be auto-created."
    )
    company = models.ForeignKey(
        "companies.Company", null=True, blank=True, on_delete=models.SET_NULL
    )
    in_office = models.BooleanField("In Office", default=False)
    first_name = models.CharField("First Name", max_length=30)
    middle_name = models.CharField("Middle Name", max_length=30, blank=True)
    maiden_name = models.CharField("Maiden Name", max_length=150, blank=True)
    last_name = models.CharField("Last Name", max_length=150)
    preferred_name = models.CharField("Preferred Name", max_length=30, blank=True)
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
    personal_email_address = models.EmailField("Personal Email Address")
    show_contact_details = models.BooleanField(
        "Show Contact Details",
        default=True
    )
    notes = models.TextField(blank=True, validators=[MaxLengthValidator(500)])

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
    # person = models.ForeignKey(
    #     "directory.Person",
    #     null=True,
    #     blank=True,
    #     limit_choices_to={"user__is_active": True},
    #     on_delete=models.CASCADE
    # )
    ip_address = models.GenericIPAddressField("IP Address")

    class Meta:
        verbose_name = "Authentication Audit"
        verbose_name_plural = "Authentication Audits"
        ordering = ["timestamp"]
        constraints = [
            models.UniqueConstraint(
                fields=["timestamp", "person", "ip_address"],
                name="authentication_audit_timestamp_person_ip_address"
            )
        ]

    def __str__(self):
        return f"{self.person} - {self.timestamp} [{self.ip_address}]"
