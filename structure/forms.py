from structure.models import Campus, Residence, Room


def get_campus_choices(json_response=None):
    if json_response:
        response = {"results": []}
    else:
        response = []

    campus_queryset = Campus.objects.all()
    for campus in campus_queryset:
        if json_response:
            response_object = {
                "id": f"{campus.pk}",
                "text": campus.name
            }
            response["results"].append(response_object)
        else:
            response.append((campus.pk, campus.name))

    return response


def get_residence_choices(campus, json_response=None):
    if json_response:
        response = {"results": []}
    else:
        response = []

    residence_queryset = Residence.objects.filter(campus=campus)
    for residence in residence_queryset:
        if json_response:
            response_object = {
                "id": f"{residence.pk}",
                "text": residence.name
            }
            response["results"].append(response_object)
        else:
            response.append((residence.pk, residence.name))
    return response


def get_room_choices(residence, json_response=None):
    if json_response:
        response = {"results": []}
    else:
        response = []

    room_queryset = Room.objects.filter(residence=residence)
    for room in room_queryset:
        if json_response:
            response_object = {
                "id": f"{room.pk}",
                "text": room.number
            }
            response["results"].append(response_object)
        else:
            response.append((room.pk, room.number))
    return response
