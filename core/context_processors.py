from django.conf import settings

from administration.models import Personnel
from api_google.constants import GOOGLE_RECAPTCHA_SITE_KEY
from core.utilities import get_date_time_now


def template_variables(request):
    """
    Here are a couple of template variables that are used in the front-end
    i.e.: templates and are available in every request / response.
    """
    request_path = request.get_full_path()
    date_display = get_date_time_now(formatting="%A, %e %B, %Y")
    person = Personnel.objects.get(student_email=request.user.username)

    variables = {
        "site_title": settings.SITE_TITLE,
        "site_version": settings.SITE_VERSION,
        "site_author": settings.SITE_AUTHOR,
        "site_description": settings.SITE_DESCRIPTION,
        "date_display": date_display,
        "person": person
    }

    # Get the application, if applicable.
    if "/administration/" not in request_path:
        breakup_path = request_path.split("/")
        if breakup_path[1]:
            application_name = breakup_path[1].replace("-", " ").title()
            variables["application"] = f"{application_name}"

            # Handle the Google reCaptcha settings.
            if request.user:
                if not request.user.is_authenticated:
                    variables["google_recaptcha_site_key"] = GOOGLE_RECAPTCHA_SITE_KEY

    return variables
