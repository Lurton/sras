from django.db import models

from core.utilities import get_document_upload_path
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


class Application(models.Model):
    class Status(models.IntegerChoices):
        SUBMITTED = 1, "Submitted"
        IN_REVIEW = 2, "In Review"
        APPROVED = 3, "Approved"
        REJECTED = 4, "Rejected"
        TERMINATED = 5, "Terminated"

    student = models.ForeignKey(
        Personnel, verbose_name="Student", on_delete=models.CASCADE
    )
    date = models.DateField()
    room = models.ForeignKey("structure.Room", on_delete=models.CASCADE, blank=False)
    resolved = models.BooleanField(default=False)
    status = models.PositiveIntegerField("Application Status", choices=Status.choices, default=Status.SUBMITTED)

    class Meta:
        verbose_name = "Application"
        verbose_name_plural = "Applications"
        ordering = ["student"]

    def __str__(self):
        return f"{self.student} - {self.room}"


class Transfer(models.Model):
    student = models.ForeignKey(
        Personnel, verbose_name="Student", on_delete=models.CASCADE
    )
    application = models.ForeignKey(Application, on_delete=models.CASCADE, blank=False)
    from_room = models.ForeignKey("structure.Room", on_delete=models.CASCADE, blank=False, related_name="%(app_label)s_%(class)s_from_room")
    to_room = models.ForeignKey("structure.Room", on_delete=models.CASCADE, blank=False, related_name="%(app_label)s_%(class)s_to_room")
    date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Transfer"
        verbose_name_plural = "Transfers"
        ordering = ["student"]
        constraints = [models.UniqueConstraint(
            fields=["student", "application", "from_room", "to_room"],
            name="transfer_student_application_from_room_to_room"
        )]


class Termination(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, blank=False)
    date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Termination"
        verbose_name_plural = "Terminations"
        ordering = ["application"]
        constraints = [models.UniqueConstraint(
            fields=["application"],
            name="termination_application"
        )]
