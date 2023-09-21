from django.urls import path, include

from . import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("password-reset/", include([
        path("", views.password_reset, name="password_reset"),
        path(
            "<uidb64>/<token>/",
            views.CorePasswordResetConfirmView.as_view(),
            name="password_reset_confirm"
        ),
        path(
            "complete/",
            views.password_reset_complete,
            name="password_reset_complete"
        )
    ]))
]
