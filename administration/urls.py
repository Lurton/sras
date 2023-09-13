from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("application/", views.application, name="application")
]
