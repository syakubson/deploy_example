"""
Script to download model folder from S3 storage.
This script runs during container startup to fetch the model files.
"""

import os
import sys

import boto3
from botocore.exceptions import ClientError


def download_folder_from_s3(
    s3_folder_name: str, s3_endpoint: str, s3_access_key: str, s3_secret_key: str, s3_bucket: str
):
    """Download entire folder from S3 bucket.

    Args:
        s3_folder_name: Name of the folder to download from S3
        s3_endpoint (str): S3 endpoint
        s3_access_key (str): S3 access key
        s3_secret_key (str): S3 secret key
        s3_bucket (str): S3 bucket
    """

    # Create model directory
    model_dir = "/app/model"
    os.makedirs(model_dir, exist_ok=True)

    try:
        s3_client = boto3.client(
            "s3", endpoint_url=s3_endpoint, aws_access_key_id=s3_access_key, aws_secret_access_key=s3_secret_key
        )
    except Exception as e:
        print(f"Error: Failed to create S3 client: {e}")
        sys.exit(1)

    # Ensure folder name ends with /
    s3_prefix = s3_folder_name if s3_folder_name.endswith("/") else f"{s3_folder_name}/"
    print(f"Downloading folder from s3://{s3_bucket}/{s3_prefix}")

    try:
        paginator = s3_client.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=s3_bucket, Prefix=s3_prefix)

        file_count = 0
        for page in pages:
            if "Contents" not in page:
                print(f"Warning: No files found in s3://{s3_bucket}/{s3_prefix}")
                continue

            for obj in page["Contents"]:
                s3_key = obj["Key"]

                # Skip folder markers
                if s3_key.endswith("/"):
                    continue

                # Calculate local file path
                relative_path = os.path.relpath(s3_key, s3_prefix)
                local_file_path = os.path.join(model_dir, relative_path)

                # Create local directory structure
                local_file_dir = os.path.dirname(local_file_path)
                os.makedirs(local_file_dir, exist_ok=True)

                # Download file
                print(f"Downloading: {s3_key} -> {local_file_path}")
                try:
                    s3_client.download_file(s3_bucket, s3_key, local_file_path)
                    file_count += 1
                except ClientError as e:
                    print(f"Error: Failed to download {s3_key}: {e}")
                    sys.exit(1)

        print(f"Successfully downloaded {file_count} files from s3://{s3_bucket}/{s3_prefix}")

    except ClientError as e:
        print(f"Error: Failed to list objects in S3: {e}")
        sys.exit(1)


if __name__ == "__main__":
    folder_name = "qwen3-0.6b/"

    s3_endpoint = os.getenv("S3_ENDPOINT", "")
    s3_access_key = os.getenv("S3_ACCESS_KEY", "")
    s3_secret_key = os.getenv("S3_SECRET_KEY", "")
    s3_bucket = os.getenv("S3_BUCKET", "")

    download_folder_from_s3(
        folder_name,
        s3_endpoint,
        s3_access_key,
        s3_secret_key,
        s3_bucket,
    )
