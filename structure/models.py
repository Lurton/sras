from django.db import models
from django.urls import reverse

from administration.models import Personnel
from core.utilities import get_document_upload_path


# Create your models here.
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

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # return reverse("structure:campus_view", args=[self.pk])
        return ""


class Residence(models.Model):
    name = models.CharField("Residence", max_length=64, unique=True)
    campus = models.ForeignKey("structure.Campus", on_delete=models.CASCADE, blank=False)
    image = models.FileField(upload_to=get_document_upload_path, null=True, blank=True)

    class Meta:
        verbose_name = "Residence"
        verbose_name_plural = "Residences"
        ordering = ["name"]
        constraints = [models.UniqueConstraint(
            fields=["name", "campus"],
            name="residence_name_campus"
        )]

    def __str__(self):
        return self.name


class Room(models.Model):
    number = models.CharField("Residence", max_length=64)
    floor = models.IntegerField("Floor")
    residence = models.ForeignKey("structure.Residence", on_delete=models.CASCADE, blank=False)
    image = models.FileField(upload_to=get_document_upload_path, null=True, blank=True)

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Room"
        ordering = ["number"]
        constraints = [models.UniqueConstraint(
            fields=["residence", "number"],
            name="room_residence_number"
        )]

    def __str__(self):
        return self.number
