#!/usr/bin/env python
import os
import sys
import django

from pathlib import Path

BASE_PATH = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(f"{BASE_PATH}")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sras.settings")

django.setup()


def create_campus_residence_rooms(campus_count: int, res_count: int, rooms_count):
    from administration.models import Campus, Residence, Room

    for i in range(campus_count):
        campus, created = Campus.objects.get_or_create(
          name=f"Campus_{i}",
          location=f"Location_{i}",
          address=f"Address_{i}",
          path=f"campus_{i}",
          email_address=f"campus_{i}@cput.ac.za"
        )

        for res in range(res_count):
            residence, created = Residence.objects.get_or_create(
                name=f"Campus_{i}_Residence_{res}",
                campus=campus
            )

            for room in range(rooms_count):
                room, created = Room.objects.get_or_create(
                    number=f"R{res}-{room}",
                    floor=res,
                    residence=residence
                )


def delete_all():
    from administration.models import Campus, Residence, Room

    campuses = Campus.objects.all()
    residences = Residence.objects.all()
    rooms = Room.objects.all()

    for each in campuses:
        each.delete()

    for each in residences:
        each.delete()

    for each in rooms:
        each.delete()


def main():
    campus_amount = 5
    res_amount = 12
    room_amount = 20

    create_campus_residence_rooms(campus_amount, res_amount, room_amount)
    # delete_all()
    print("Done!")


if __name__ == "__main__":
    main()
