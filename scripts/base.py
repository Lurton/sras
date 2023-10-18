#!/usr/bin/env python
import os
import sys
import django

from pathlib import Path

BASE_DIRECTORY = Path(__file__).resolve(strict=True).parent.parent

sys.path.append(f"{BASE_DIRECTORY}")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sras.settings")

django.setup()


def main():
    # import socket
    # host_name = socket.gethostname()
    # ip_address = socket.gethostbyname(host_name)
    #
    # print(f"hostname: {host_name}")
    # print(f"ip address: {ip_address}")

    from core.utilities import send_email
    from core.models import USER_MODEL
    from core.utilities import get_date_time_now
    from django.contrib.auth.tokens import default_token_generator
    from django.utils.encoding import force_bytes
    from django.utils.formats import date_format
    from django.utils.http import urlsafe_base64_encode

    now = get_date_time_now()
    user = USER_MODEL.objects.get(email="215169115@mycput.ac.za")
    timestamp = date_format(now, "DATETIME_FORMAT", use_l10n=False)

    recipient = "215169115@mycput.ac.za"
    subject = "Subject"
    template = "email/password-reset-confirmation.html"
    email_data = {
        "subject": subject,
        "full_name": f"Argus Ndabashinze",
        "timestamp": f"{timestamp}",
        "uid": urlsafe_base64_encode(force_bytes(2)),
        "token": default_token_generator.make_token(user)
    }

    send_email(recipient, subject, template, email_data)

    print("Done!")


if __name__ == "__main__":
    main()
