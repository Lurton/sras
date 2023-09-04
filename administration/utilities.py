from administration.constants import (
    MEDIA_PERSONNEL_PREFIX, MEDIA_CAMPUS_PREFIX, MEDIA_RESIDENCE_PREFIX,
    MEDIA_ROOM_PREFIX
)


def get_document_upload_path(instance, filename):
    """
    This is the default directory to upload any documents to on AWS S3.
    """
    from administration.models import Personnel, Campus, Residence, Room

    full_document_path = []
    prefix = None

    if isinstance(instance, Personnel):
        prefix = MEDIA_PERSONNEL_PREFIX + f"{instance.student_number}"
        image_extension = str(filename.split(".")[-1]).lower()
        filename = f"{instance.student_number}.{image_extension}"

    if isinstance(instance, Campus):
        prefix = MEDIA_CAMPUS_PREFIX + f"{instance.name}"
        image_extension = str(filename.split(".")[-1]).lower()
        filename = f"{instance.name}.{image_extension}"

    if isinstance(instance, Residence):
        prefix = MEDIA_RESIDENCE_PREFIX + f"{instance.name}"
        image_extension = str(filename.split(".")[-1]).lower()
        filename = f"{instance.name}.{image_extension}"

    if isinstance(instance, Room):
        prefix = MEDIA_ROOM_PREFIX + f"{instance.number}"
        image_extension = str(filename.split(".")[-1]).lower()
        filename = f"{instance.number}.{image_extension}"

    full_document_path.append(prefix)
    full_document_path.append(filename)

    return "/".join(full_document_path)


def generate_student_number(student):
    student_number = student.student_email.strip("@")[0]

    return student_number
