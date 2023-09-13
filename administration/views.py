from django.shortcuts import render
from django.contrib import messages


# Create your views here.
def application(request, template_name="administration/application.html"):

    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():

            messages.success(
                request,
                "Your account and profile information have been created"
                " successfully!"
            )

        else:
            messages.error(
                request,
                "There was an error while trying to register the account and"
                " profile. Please try again!"
            )
    else:
        form = RegistrationForm()

    return TemplateResponse(request, template_name, {"form": form})