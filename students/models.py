from django.db import models
from django.urls import reverse

from core.models import BaseUserAuthentication


# Create your models here.
class Student(BaseUserAuthentication):
    image = models.FileField(
        upload_to=get_document_upload_path,
        null=True,
        blank=True
    )
    superbalist_account = models.PositiveIntegerField(
        "Superbalist Account",
        default=0
    )
    care_of_intermediary = models.CharField(
        "Care of Intermediary",
        max_length=64,
        blank=True
    )
    budget_job_number = models.CharField(
        "Budget Job Number",
        max_length=20,
        blank=True
    )
    location = models.ForeignKey(
        "human_resources.Location",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "Person"
        ordering = ["last_name", "first_name"]

    @property
    def get_student_number(self):
        return self.code

    @property
    def get_email_address(self):
        if self.get_primary_email:
            return self.get_primary_email
        if self.personal_email_address:
            return self.personal_email_address
        return None

    @property
    def get_physical_address(self):
        try:
            return PhysicalAddress.objects.get(person=self)
        except PhysicalAddress.DoesNotExist:
            pass
        return None

    def get_absolute_url(self):
        return reverse(
            "human_resources_people_view",
            args=[self.company.path, self.pk]
        )

    def __str__(self):
        preferred_name = self.preferred_name
        if preferred_name:
            return f"{preferred_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"