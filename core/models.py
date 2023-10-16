from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator, EMPTY_VALUES
from django.db import models

from django_extensions.db.models import TimeStampedModel

from administration.models import Personnel
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
                fields=["timestamp", "ip_address"],
                name="authentication_audit_timestamp_ip_address"
            )
        ]

    def __str__(self):
        return f"{self.timestamp} [{self.ip_address}]"


class PhysicalAddress(BasePhysicalAddress):
    person = models.ForeignKey(
        Personnel,
        blank=False,
        null=True,
        on_delete=models.CASCADE
    )
    unit_number = models.CharField("Unit Number", max_length=16, blank=True)
    complex_name = models.CharField("Complex Name", max_length=128, blank=True)
    street_number = models.CharField("Street Number", max_length=16, blank=True)
    street_name = models.CharField("Street Name", max_length=128, blank=True)
    suburb = models.CharField(max_length=128, blank=True)

    class Meta:
        verbose_name = "Physical Address"
        verbose_name_plural = "Physical Addresses"
        ordering = ["person"]

    @property
    def full_physical_address(self):
        address_list = []
        if self.unit_number and self.complex_name:
            address_list.append(f"{self.unit_number} {self.complex_name}")
        elif self.complex_name and not self.unit_number:
            address_list.append(f"{self.complex_name}")
        elif self.unit_number and not self.complex_name:
            address_list.append(f"{self.unit_number}")
        if self.street_number and self.street_name:
            address_list.append(f"{self.street_number} {self.street_name}")
        elif self.street_name and not self.street_number:
            address_list.append(f"{self.street_name}")
        if self.suburb:
            address_list.append(self.suburb)
        initial_address = ", ".join(address_list)
        if address_list not in EMPTY_VALUES:
            address = f"{initial_address}, {self.get_full_address}"
        else:
            address = f"{self.get_full_address}"
        return address

    def __str__(self):
        return f"{self.full_physical_address}"
