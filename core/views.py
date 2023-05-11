from django.template.response import TemplateResponse


def index(request, template_name="core/index.html"):
    """
    This is the landing welcome page of the system.
    """
    if request.user:
        if request.user.is_authenticated:
            # return redirect("core:dashboard")
            pass
    return TemplateResponse(request, template_name)
