from django.urls import path, include

from . import views

app_name = "administration"

urlpatterns = [
    path("application/", views.application, name="application"),
    path("ajax/", include([
        path(
            "residences/",
            views.ajax_residences,
            name="ajax_residences"
        ),
        path(
            "rooms/",
            views.ajax_rooms,
            name="ajax_rooms"
        )
    ]))
]
