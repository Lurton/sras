import json
import logging

from django.conf import settings

from api.aws.authentication import aws_client, aws_resource
from api.aws.utitlies import AWSCloudFrontThread

LOGGER = logging.getLogger(__name__)


def aws_s3_bucket(bucket_name):
    """
    This function returns the bucket object specified in the parameter. The
    default is "takealotgroup.team", however a different bucket name can be passed
    in if required.
    """
    credentials = settings.CONFIG.get("setup").get("aws").get("s3")
    resource = aws_resource("s3", credentials)

    try:
        return resource.Bucket(bucket_name)
    except Exception:
        LOGGER.critical("aws_s3_bucket", exc_info=True)


def aws_s3_object_get(file_name):
    """
    This function returns an AWS object.
    """
    credentials = settings.CONFIG.get("setup").get("aws").get("s3")
    bucket_name = credentials.get("bucket")

    # Get the respective AWS S3 bucket that we are working in.
    bucket = aws_s3_bucket(bucket_name)

    # Now we try to get the file object.
    try:
        return bucket.Object(file_name)
    except Exception:
        LOGGER.critical("aws_s3_object_get", exc_info=True)


def aws_s3_move_file(source=None, destination=None, delete=True):
    """
    This function moves the file from the given source to the given destination,
    within the given bucket. The default "delete" parameter is `True`.
    Pass in `False` if you want the function to copy the files without deleting
    them in the original location.
    `source` refers to the file path of the file to be moved.
    `destination` refers to the file path of the location the file must be moved
    to. Both `source` & `destination` must include the file name and extension.
    i.e.: the full prefix or key.
    """
    credentials = settings.CONFIG.get("setup").get("aws").get("s3")
    bucket_name = credentials.get("bucket")

    # Get the respective AWS S3 bucket that we are working in.
    bucket = aws_s3_bucket(bucket_name)

    # Now we filter the bucket to return only the file we would like to
    # move (the source).
    # We create a dictionary describing the location of the source file.
    # This must be passed into the copy_object function below.
    copy_source = {
        "Bucket": bucket_name,
        "Key": source
    }

    # Now we try to copy the file to the destination.
    try:
        bucket.copy(
            copy_source,
            destination,
            ExtraArgs={
                "StorageClass": "STANDARD_IA",
                "MetadataDirective": "COPY"
            }
        )

        # If the copy was successful, we delete the file in the bucket.
        if delete:
            resource = aws_resource("s3", credentials)
            aws_s3_object = resource.Object(bucket_name, source)
            aws_s3_object.delete()

        return True

    except Exception:
        LOGGER.critical("aws_s3_move_file", exc_info=True)

    return False


def aws_cloudfront_invalidate(full_object_path):
    """
    This function invalidates a specific object (file) from CloudFront.
    Note, this only happens in production.
    """
    if not settings.DEBUG:
        try:
            AWSCloudFrontThread(full_object_path).start()
        except Exception:
            LOGGER.critical(
                "There was a problem invalidating the CloudFront object (file) on AWS.",
                exc_info=True
            )
        return full_object_path


def aws_invoke_lambda(payload: dict, function_name: str, invocation_type: str = "RequestResponse"):
    """
    Invokes an AWS Lambda function.
    params: payload dict
    params: function_name The AWS Lamda function name.
    params: invocation_type str "RequestResponse" (default), "Event", "DryRun"
    """
    client = aws_client("lambda")

    try:
        response = client.invoke(
            FunctionName=function_name,
            InvocationType=invocation_type,
            LogType="None",
            Payload=json.dumps(payload)
        )
        return json.loads(response["Payload"].read().decode("utf-8"))

    except Exception:
        LOGGER.critical("aws_invoke_lambda", exc_info=True)


def aws_textract_analyze_id(s3_source=None, local_source=None) -> dict or None:
    """
    This function retrieves an S3 file object or processes a local file and
    analyzes it to extract key value pairs from an identification document.
    params: s3_source S3_document_key or None
    params: local_source local file location or None
    returns: dict
    """
    client = aws_client("textract")

    # We create a list of dictionaries describing the location of the source file.
    # This must be passed into the analyze_id function below.
    document_pages = []
    if s3_source:
        bucket_name = settings.CONFIG.get("setup").get("aws").get("s3").get("bucket")
        document_pages.append(
            {
                "S3Object": {
                    "Bucket": bucket_name,
                    "Name": s3_source
                }
            }
        )
    elif local_source:
        with open(local_source, "rb") as image2string:
            data_string = bytearray(image2string.read())
            document_pages.append(
                {
                    "Bytes": data_string
                }
            )

    # Try to analyze the source object.
    try:
        return client.analyze_id(DocumentPages=document_pages)
    except Exception:
        LOGGER.critical("aws_textract_analyze_document", exc_info=True)


def aws_publish_text_message(phone_number, message) -> dict:
    """
    Publishes a text message directly to a phone number without the need for a
    subscription.

    :param phone_number: The phone number that receives the message. This must be
                         in E.164 format. For example, +27841234567.
    :param message: The message to send.
    :return: a dict with the `status` of the response (bool) and the AWS SNS `message_id` (str).
    """
    credentials = settings.CONFIG.get("setup").get("aws").get("sns")
    sns_client = aws_client("sns", credentials)
    response = {
        "status": False,
        "message_id": None
    }

    try:
        request = sns_client.publish(
            PhoneNumber=phone_number, Message=message,
            MessageAttributes={
                "AWS.SNS.SMS.SenderID": {
                    "DataType": "String",
                    "StringValue": "Takealot-Gr"
                },
                "AWS.SNS.SMS.SMSType": {
                    "DataType": "String",
                    "StringValue": "Transactional"
                }
            }
        )
        message_id = request["MessageId"]
        response["message_id"] = message_id
        LOGGER.info(f"Published message: {message_id} to {phone_number}.")
        if request["ResponseMetadata"]["HTTPStatusCode"] == 200:
            response["status"] = True

    except Exception:
        # Multiple SMS messages could be sent at once, therefore we catch all exceptions.
        LOGGER.exception(f"`publish_text_message` | Error sending SMS to {phone_number}.")

    return response
