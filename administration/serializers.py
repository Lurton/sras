from django.db.models import Q
from django.http import JsonResponse
from rest_framework import serializers

from administration.models import Application
from core.utilities import list_view


class ApplicationsListSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()
    student = serializers.StringRelatedField()
    date = serializers.SerializerMethodField()
    campus = serializers.SerializerMethodField()
    residence = serializers.SerializerMethodField()
    room = serializers.StringRelatedField()

    class Meta:
        model = Application
        fields = ["id", "absolute_url", "student", "date", "campus", "residence", "room"]

    @staticmethod
    def get_absolute_url(obj):
        return obj.get_absolute_url()

    @staticmethod
    def get_date(obj):
        return obj.date

    @staticmethod
    def get_campus(obj):
        return obj.room.residence.campus

    @staticmethod
    def get_residence(obj):
        return obj.room.residence


def get_applications_serialized_data(
    request,
    search_value=None
):
    """
    This helper function is used as a central point to initialize all
    residences for a given campus.
    options: for example, the list of columns that will be displayed in the
    table, which must match the serialized data that is returned below.
    Essentially it provides a one-stop-shop and is called directly from the view
    which returns the appropriate JSON response.
    """
    # base queryset.
    queryset = Application.objects.filter(status=Application.Status.SUBMITTED)

    # This is to further `filter / search` the above queryset based on the table
    # search input.
    if search_value:
        queryset = queryset.filter(
            Q(student__first_name__icontains=search_value)
            | Q(student__first_name__icontains=search_value)
            | Q(room__number__icontains=search_value)
        )

    # The pagination and object list preparations.
    object_list = list_view(
        request, queryset
    )

    # The rest framework serializer method.
    serializer = ApplicationsListSerializer(
        object_list["queryset"], many=True
    )

    # The JSON response.
    serialized_data = {
        "draw": object_list["draw"],
        "recordsTotal": len(queryset),
        "recordsFiltered": object_list["recordsFiltered"],
        "data": serializer.data
    }

    return JsonResponse(serialized_data, safe=False)
