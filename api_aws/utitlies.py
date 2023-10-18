import threading

from django.conf import settings

from api.aws.authentication import aws_client
from core.utilities import generate_timestamp


class AWSCloudFrontThread(threading.Thread):
    """
    This class invalidates objects threading via the AWS CloudFront service.
    """
    def __init__(self, full_object_path):
        threading.Thread.__init__(self)
        self.full_object_path = full_object_path

    def run(self):
        # First retrieve the AWS CloudFront client.
        credentials = settings.CONFIG.get("setup").get("aws").get("cloudfront")
        aws_cloudfront_client = aws_client("cloudfront", credentials)

        # Now try to invalidate the object.
        aws_cloudfront_client.create_invalidation(
            DistributionId=credentials.get("distribution_id"),
            InvalidationBatch={
                "Paths": {
                    "Quantity": 1,
                    "Items": [
                        self.full_object_path
                    ]
                },
                "CallerReference": generate_timestamp()
            }
        )
