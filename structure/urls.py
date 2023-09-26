from django.urls import path, include

from . import views

app_name = "structure"

urlpatterns = [
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
    ])),
    path("campus/", include([
        path(
            "",
            views.campus_list,
            name="campus_list"
        ),
        # path(
        #     "add/",
        #     views.campus_add,
        #     name="campus_add"
        # ),
        path("<int:campus_pk>/", include([
            path(
                "view/",
                views.campus_view,
                name="campus_view"
            ),
            path(
                "edit/",
                views.campus_edit,
                name="campus_edit"
            )
        ]))
    ])),
    path("residence/", include([
        path(
            "",
            views.residence_list,
            name="residence_list"
        ),
        path("<int:residence_pk>/", include([
            path(
                "view/",
                views.residence_view,
                name="residence_view"
            ),
            path(
                "edit/",
                views.residence_edit,
                name="residence_edit"
            )
        ]))
    ])),
    path("room/", include([
        path(
            "",
            views.room_list,
            name="room_list"
        ),
        path("<int:room_pk>/", include([
            path(
                "view/",
                views.room_view,
                name="room_view"
            ),
            path(
                "edit/",
                views.room_edit,
                name="room_edit"
            )
        ]))
    ]))
]
