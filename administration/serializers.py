from django.db.models import Q
from django.http import JsonResponse

from rest_framework import serializers

from administration.models import Residence, Campus, Room
from core.utilities import list_view


class RoomListSerializer(serializers.ModelSerializer):
    number = serializers.StringRelatedField()
    floor = serializers.StringRelatedField()
    residence = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ["number", "floor", "residence"]

    @staticmethod
    def get_residence(obj):
        return obj.residence.name


class ResidenceListSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField()
    campus = serializers.SerializerMethodField()

    class Meta:
        model = Residence
        fields = ["name", "campus"]

    @staticmethod
    def get_campus(obj):
        return obj.campus.name


class CampusListSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField()

    class Meta:
        model = Campus
        fields = ["name"]


def get_campus_serialized_data(
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
    queryset = Campus.objects.all()

    # This is to further `filter / search` the above queryset based on the table
    # search input.
    if search_value:
        queryset = queryset.filter(
            name__icontains=search_value
        )

    # The pagination and object list preparations.
    object_list = list_view(
        request, queryset
    )

    # The rest framework serializer method.
    serializer = CampusListSerializer(
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


def get_residences_serialized_data(
    request,
    campus,
    search_parameters=None,
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
    search_parameters["campus"] = campus

    # base queryset.
    queryset = Residence.objects.filter(**search_parameters)

    # This is to further `filter / search` the above queryset based on the table
    # search input.
    if search_value:
        queryset = queryset.filter(
            Q(name__icontains=search_value) |
            Q(campus__name__icontains=search_value)
        )

    # The pagination and object list preparations.
    object_list = list_view(
        request, queryset.order_by("-campus")
    )

    # The rest framework serializer method.
    serializer = ResidenceListSerializer(
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


def get_rooms_serialized_data(
    request,
    residence,
    search_parameters=None,
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
    search_parameters["residence"] = residence

    # base queryset.
    queryset = Residence.objects.filter(**search_parameters)

    # This is to further `filter / search` the above queryset based on the table
    # search input.
    if search_value:
        queryset = queryset.filter(
            Q(number__icontains=search_value) |
            Q(residence__name__icontains=search_value)
        )

    # The pagination and object list preparations.
    object_list = list_view(
        request, queryset.order_by("residence")
    )

    # The rest framework serializer method.
    serializer = RoomListSerializer(
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
