#!/usr/bin/env python
import os
import sys
import django

from pathlib import Path

BASE_PATH = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(f"{BASE_PATH}")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings.debug")

django.setup()

from api.aws.authentication import (
    aws_config, aws_session, aws_client, aws_resource
)


def test_aws_session():
    response = aws_session()
    print("aws_session", response)


def test_aws_client():
    service_name = "s3"
    credentials = {
        "aws_access_key_id": "",
        "aws_secret_access_key": ""
    }
    response = aws_client(service_name, credentials)
    print("aws_client", response)


def test_aws_resource():
    service_name = "s3"
    credentials = {
        "aws_access_key_id": "",
        "aws_secret_access_key": ""
    }
    response = aws_resource(service_name, credentials)
    print("aws_resource", response)


def test_aws_config():
    response = aws_config("takealotgroup.team")
    print("aws_config", response)


if __name__ == "__main__":
    # test_aws_session()
    # test_aws_client()
    # test_aws_resource()
    # test_aws_config()

    print("Done!")
