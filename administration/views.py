from django.contrib import messages
from django.template.response import TemplateResponse

from administration.forms import ApplicationForm


# Create your views here.
def application(request, template_name="administration/application.html"):

    if request.method == "POST":
        form = ApplicationForm(request.POST)

        if form.is_valid():

            messages.success(
                request,
                "Your application has been submitted successfully!"
            )

        else:
            messages.error(
                request,
                "There was an error while trying to submit your application"
            )
    else:
        form = ApplicationForm()

    return TemplateResponse(request, template_name, {"form": form})
