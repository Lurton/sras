#!/usr/bin/env python
import os
import sys
import django

from pathlib import Path


BASE_DIRECTORY = Path(__file__).resolve(strict=True).parent.parent

sys.path.append(f"{BASE_DIRECTORY}")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sras.settings")

django.setup()


def create_residence_admin():
    from administration.models import Personnel
    from django.contrib.auth import get_user_model
    from django.contrib.auth.hashers import make_password

    admin, created = Personnel.objects.get_or_create(
        first_name="Residence",
        last_name="Administrator",
        student_email="admin@mycput.ac.za",
        personnel_type=Personnel.Type.ADMIN
    )

    user_model = get_user_model()
    password = make_password("LetMeIn")
    user_account = user_model.objects.create(
        first_name=admin.first_name,
        last_name=admin.last_name,
        username=admin.student_email,
        email=admin.student_email,
        password=password,
        is_active=True
    )
    
def main():
    print("Done!")


if __name__ == "__main__":
    main()
