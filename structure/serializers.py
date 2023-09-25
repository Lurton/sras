from django.db.models import Q
from django.http import JsonResponse

from rest_framework import serializers

from structure.models import Residence, Campus, Room
from core.utilities import list_view


class RoomListSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()
    number = serializers.StringRelatedField()
    floor = serializers.StringRelatedField()
    residence = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ["id", "absolute_url", "number", "floor", "residence"]

    @staticmethod
    def get_absolute_url(obj):
        return obj.get_absolute_url()

    @staticmethod
    def get_residence(obj):
        return obj.residence.name


class ResidenceListSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()
    name = serializers.StringRelatedField()
    campus = serializers.SerializerMethodField()

    class Meta:
        model = Residence
        fields = ["id", "absolute_url", "name", "campus"]

    @staticmethod
    def get_absolute_url(obj):
        return obj.get_absolute_url()

    @staticmethod
    def get_campus(obj):
        return obj.campus.name


class CampusListSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()
    name = serializers.StringRelatedField()
    location = serializers.StringRelatedField()
    address = serializers.StringRelatedField()
    email_address = serializers.StringRelatedField()

    class Meta:
        model = Campus
        fields = ["id", "absolute_url", "name", "location", "address", "email_address"]

    @staticmethod
    def get_absolute_url(obj):
        return obj.get_absolute_url()


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
            Q(name__icontains=search_value)
            | Q(location__icontains=search_value)
            | Q(address__icontains=search_value)
            | Q(email_address__icontains=search_value)
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
    # base queryset.
    queryset = Room.objects.filter(**search_parameters)

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
