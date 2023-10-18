from storages.backends.s3boto3 import S3Boto3Storage


class AWSS3StaticStorage(S3Boto3Storage):
    location = "static"


class AWSS3MediaStorage(S3Boto3Storage):
    location = "media"


# The AWS QuickSight Information.
AWS_QUICKSIGHT_DEFAULT_SESSION_LIMIT = 30

# Headcount by Race
AWS_QUICKSIGHT_DASHBOARD_1 = "d2fb2e6e-3e72-47b2-8a60-9bfa432ff086"
# Demographic Analysis
AWS_QUICKSIGHT_DASHBOARD_2 = "29d3502b-978d-4e42-8a8a-ff95c958b402"
# Performance Ratings
AWS_QUICKSIGHT_DASHBOARD_3 = "f95bee9c-8d88-4c3f-aae3-ad586c0c9d0a"

AWS_QUICKSIGHT_DASHBOARD_LIST = [
    AWS_QUICKSIGHT_DASHBOARD_1,
    AWS_QUICKSIGHT_DASHBOARD_2,
    AWS_QUICKSIGHT_DASHBOARD_3
]

# Default AWS S3 base folders or paths and file prefixes.
AWS_S3_MEDIA_ROOT = "media/"
AWS_S3_MEDIA_TRASH_ROOT = AWS_S3_MEDIA_ROOT + "trash/"
AWS_S3_MEDIA_ANNOUNCEMENT_PREFIX = "announcements/"
AWS_S3_MEDIA_PERSON_PREFIX = "people/"
AWS_S3_MEDIA_GUIDES_PREFIX = "guides/"
AWS_S3_MEDIA_REMUNERATION_PREFIX = "remuneration/"
AWS_S3_MEDIA_RATING_PREFIX = "ratings/"
AWS_S3_MEDIA_BUDGETS_PREFIX = "budgets/"
AWS_S3_MEDIA_COUPONS_PREFIX = "coupons/"
AWS_S3_MEDIA_TEXTRACT_PREFIX = "textract/"
AWS_S3_MEDIA_PERFORMANCE_ASSESSMENTS_PREFIX = "performance-assessments/"

# Limit uploads to ~10MB [10000000] and they must be in the allowed mime
# types for documents.
AWS_S3_MAX_UPLOAD_SIZE = 10000000
AWS_S3_ALLOWED_CONTENT_EXTENSIONS = [
    "jpg", "jpeg", "png", "pdf", "xls", "xlsx", "doc", "docx", "ppt",
    "pptx", "thmx"
]
AWS_S3_ALLOWED_CONTENT_TYPES = [
    "image/jpeg", "image/png", "application/pdf", "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "application/vnd.ms-powerpoint", "application/vnd.ms-officetheme",
    "application/msword", "text/csv"
]
