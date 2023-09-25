#!/usr/bin/env python
import os
import sys
import django

from pathlib import Path

BASE_DIRECTORY = Path(__file__).resolve(strict=True).parent.parent

sys.path.append(f"{BASE_DIRECTORY}")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings.debug")

django.setup()


def main():
    import socket
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)

    print(f"hostname: {host_name}")
    print(f"ip address: {ip_address}")

    print("Done!")


if __name__ == "__main__":
    main()
