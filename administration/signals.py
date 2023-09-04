from django.db.models.signals import pre_save
from django.dispatch import receiver

from administration.models import Personnel
from administration.utilities import generate_student_number


@receiver(pre_save, sender=Personnel)
def pre_save_personnel(sender, instance, **kwargs):
    instance.student_number = generate_student_number(instance)
