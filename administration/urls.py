from django.urls import path, include

from . import views

app_name = "administration"

urlpatterns = [
    path("application/", views.application, name="application")
]
