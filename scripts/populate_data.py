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
    from administration.models import Campus

    for i in campus_count:
        Campus.objects.create(
          name=f"Campus_{i}",
          location=f"Location_{i}",
          address=f"Address_{i}",
          path=f"campus_{i}",
          email_address=f"campus_{i}@cput.ac.za"
        )


def main():

    print("Done!")


if __name__ == "__main__":
    main()
