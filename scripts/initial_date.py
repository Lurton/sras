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


def create_residence_campuses():
    from structure.models import Campus
    from structure.models import Residence

    campuses = ["Bellville Campus", "District Six Campus", "Granger Bay Campus", "Mowbray Campus", "Wellington Campus"]

    bellville_campus, created = Campus.objects.get_or_create(
        name=f"Bellville Campus",
        location=f"Bellville",
        address=f"Symphony Way Bellville",
        email_address=f"bellvilleresidence@cput.ac.za"
    )

    district_campus, created = Campus.objects.get_or_create(
        name=f"District Six Campus",
        location=f"District Six",
        address=f"Corner of Hanover and Tennant Street Zonnebloem",
        email_address=f"districsixresidence@cput.ac.za"
    )

    granger_campus, created = Campus.objects.get_or_create(
        name=f"Granger Bay Campus",
        location=f"Granger Bay",
        address=f"Corner of Hanover and Tennant Street Zonnebloem",
        email_address=f"districsixresidence@cput.ac.za"
    )

    mowbray_campus, created = Campus.objects.get_or_create(
        name=f"Mowbray Campus",
        location=f"Mowbray",
        address=f"Highbury Road Mowbray",
        email_address=f"mowbrayresidence@cput.ac.za"
    )

    wellington_campus, created = Campus.objects.get_or_create(
        name=f"Wellington Campus",
        location=f"Wellington",
        address=f"Jan van Riebeeck Street Wellington",
        email_address=f"wellingtonresidence@cput.ac.za"
    )

    bellville_res = ["Anglo American Residence", "De Beers Residence (East Wing)", "De Goede Hoop Residence", "Freedom Square Residence", "Heroes House"]
    district_res = ["Cape Suites", "Catsville (Groote Schuur)", "City Edge Residence", "Downtown Lodge Res- Zonnebloem", "Elizabeth Women's Residence (Gardens)"]
    mowbray_res = ["Viljoenhof Residence"]
    wellington_res = ["House Bliss", "House Meiring", "Murray House", "House Navarre", "Wouter Malan"]
    granger_res = ["Victria Residence", "Johnson Residence", "Kingsley Residence"]

    for name in bellville_res:
        res, created = Residence.objects.get_or_create(
            name=name,
            campus=bellville_campus
        )

    for name in district_res:
        res, created = Residence.objects.get_or_create(
            name=name,
            campus=district_campus
        )

    for name in mowbray_res:
        res, created = Residence.objects.get_or_create(
            name=name,
            campus=mowbray_campus
        )

    for name in wellington_res:
        res, created = Residence.objects.get_or_create(
            name=name,
            campus=wellington_campus
        )

    for name in granger_res:
        res, created = Residence.objects.get_or_create(
            name=name,
            campus=granger_campus
        )


def create_rooms():
    from structure.models import Room, Residence
    import random

    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]

    residences = Residence.objects.all()

    for res in residences:
        random1 = random.randint(0, 12)
        random2 = random.randint(0, 12)
        i = 1
        while i < 10:
            room, created = Room.objects.get_or_create(
                number=f"{letters[random1]}{letters[random2]}_{i}",
                floor=1,
                residence=res
            )
            i = i+1



def main():
    create_residence_admin()
    create_residence_campuses()
    create_rooms()
    print("Done!")


if __name__ == "__main__":
    main()
