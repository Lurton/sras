from django.urls import path, include

from . import views

app_name = "administration"

urlpatterns = [
    path("application/", views.application, name="application"),
    path("transfer/", views.transfer, name="transfer"),
    path("terminate/", views.terminate, name="terminate"),
    path("applications-list/", views.applications_list, name="applications_list"),
]
