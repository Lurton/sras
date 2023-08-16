"""
This middleware is processed on each request / response cycle, and it tries to
get the respective user's / person's details `request.user` object.

If authentication has taken place, then add them to the request.

Additionally, we perform all permission checks to allow or deny certain actions
from taking place.
"""

DEFAULT_PERMISSIONS = {}


def person_permissions_check() -> dict:
    """
    This checks the requesting path (url) against permissions etc. for access
    to the various views i.e.: backend. It also checks the Person object
    against permissions etc. for visual display on the frontend.
    """
    permissions = DEFAULT_PERMISSIONS
    permissions["remuneration"] ={
    "residence_can_view_xxx": False
}

    return permissions


class UserPersonPermissionMiddleware:
    """
    On each request / response cycle we check if the user / person object has
    the necessary permissions:
    - to a particular "application" or "url / path" i.e.: backend.
    - visually for display purposes in the frontend.

    Note: All `row-level` permissions are handled via the `decorators` on each
    view respectively. In addition, all filtered querysets are handled in the
    `utilities` / `filters` / `search` methods.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user:
            if request.user.is_authenticated:
                request_path = request.path

                if request_path.startswith("/administration/"):
                    if request.user.is_staff:
                        return self.get_response(request)

                # The base `user_object` which is added to the request.
                person = request.user
                user_object = {
                    "person": person, "permissions": DEFAULT_PERMISSIONS
                }

                try:
                    # Check the path/url for permissions access and return the
                    # default visual permissions for the profile.
                    user_object["permissions"] = person_permissions_check()
                except AttributeError:
                    pass

                # N.B.: The below `request` modification is critical to the
                # proper functioning of the system.

                # Update the request with the `user_object`.
                request.user_object = user_object

        return self.get_response(request)
