from uuid import uuid4

import boto3
from botocore.client import Config

from src.core.config import get_settings

settings = get_settings()

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
    region_name=settings.aws_region,
    config=Config(signature_version="s3v4"),
)


def upload_file_to_s3(file_obj, filename, bucket=None):
    if bucket is None:
        bucket = settings.aws_s3_bucket_name

    unique_name = f"{uuid4().hex}_{filename}"
    s3_client.upload_fileobj(
        file_obj, bucket, unique_name
    )

    return f"https://{bucket}.s3.{settings.aws_region}.amazonaws.com/{unique_name}"
