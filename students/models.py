from django.db import models
from django.urls import reverse

from core.models import BaseUserAuthentication


# Create your models here.
class Student(BaseUserAuthentication):
    student_number = models.CharField(
        "Student Number",
        max_length=9,
        blank=False
    )

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
