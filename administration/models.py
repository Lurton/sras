from django.db import models

from administration.utilities import get_document_upload_path
from core.models import BaseUserAuthentication


# Create your models here.
class Personnel(BaseUserAuthentication):
    class Type(models.IntegerChoices):
        STUDENT = 0, "Student"
        ADMIN = 1, "Administrator"

    student_number = models.CharField(
        "Student Number",
        max_length=9,
        blank=False,
        unique=True
    )
    personnel_type = models.PositiveIntegerField(choices=Type.choices)
    image = models.FileField(upload_to=get_document_upload_path, null=True, blank=True)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Student"
        ordering = ["last_name", "first_name"]

    @property
    def get_student_number(self):
        return self.student_number

    def get_absolute_url(self):
        # return reverse(
        #     "students_student_view",
        #     args=[self.campus.path, self.pk]
        # )
        pass

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Campus(models.Model):
    name = models.CharField("Campus", max_length=64, unique=True)
    location = models.CharField("Location", max_length=64)
    address = models.CharField("Address", max_length=128)
    path = models.CharField(max_length=32, unique=True)
    email_address = models.EmailField(
        "Email Address",
        blank=True,
        null=True,
        help_text="This is the mailing group email address for the campus."
    )
    image = models.FileField(upload_to=get_document_upload_path, null=True, blank=True)

    class Meta:
        verbose_name = "Campus"
        verbose_name_plural = "Campuses"
        ordering = ["name"]
        constraints = [models.UniqueConstraint(
            fields=["name"],
            name="campus_name"
        )]


class Residence(models.Model):
    name = models.CharField("Residence", max_length=64, unique=True)
    campus = models.ForeignKey("administration.Campus", on_delete=models.CASCADE, blank=False)
    image = models.FileField(upload_to=get_document_upload_path, null=True, blank=True)

    class Meta:
        verbose_name = "Residence"
        verbose_name_plural = "Residences"
        ordering = ["name"]
        constraints = [models.UniqueConstraint(
            fields=["name", "campus"],
            name="residence_name_campus"
        )]


class Room(models.Model):
    number = models.CharField("Residence", max_length=64)
    floor = models.IntegerField("Floor")
    residence = models.ForeignKey("administration.Residence", on_delete=models.CASCADE, blank=False)
    image = models.FileField(upload_to=get_document_upload_path, null=True, blank=True)

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Room"
        ordering = ["number"]
        constraints = [models.UniqueConstraint(
            fields=["residence", "number"],
            name="room_residence_number"
        )]


class Application(models.Model):
    class Status(models.IntegerChoices):
        SUBMITTED = 0, "Submitted"
        IN_REVIEW = 1, "In Review"
        APPROVED = 2, "Approved"
        REJECTED = 3, "Rejected"

    student = models.ForeignKey(
        Personnel, verbose_name="Student", on_delete=models.CASCADE
    )
    date = models.DateField()
    room = models.ForeignKey("administration.Room", on_delete=models.CASCADE, blank=False)
    resolved = models.BooleanField(default=False)
    status = models.PositiveIntegerField("Application Status",choices=Status.choices ,default=Status.SUBMITTED)
