import logging
import requests

from api_google.constants import (
    GOOGLE_RECAPTCHA_SECRET_KEY, GOOGLE_RECAPTCHA_VERIFY_ENDPOINT
)

LOGGER = logging.getLogger(__name__)


def verify_recaptcha(token: str, client_ip_address: str):
    """
    Verify the Google reCaptcha token from the form submission.
    https://developers.google.com/recaptcha/docs/verify
    """
    # The payload to send to the api.
    payload = {
        "secret": GOOGLE_RECAPTCHA_SECRET_KEY,
        "response": token,
        "remoteip": client_ip_address
    }

    # Call the Google reCaptcha verify API.
    try:
        request = requests.post(GOOGLE_RECAPTCHA_VERIFY_ENDPOINT, params=payload)

        # If the request was successful, no exceptions will be raised.
        request.raise_for_status()

        return request.json()

    except Exception:
        LOGGER.exception("verify_recaptcha")