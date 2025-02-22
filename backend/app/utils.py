import json
import logging
import os
from datetime import datetime
from typing import Any, Literal

import boto3
from app.repositories.models.custom_bot_guardrails import BedrockGuardrailsModel
from botocore.client import Config
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

REGION = os.environ.get("REGION", "eu-central-1")
BEDROCK_REGION = os.environ.get("BEDROCK_REGION", "eu-central-1")
PUBLISH_API_CODEBUILD_PROJECT_NAME = os.environ.get(
    "PUBLISH_API_CODEBUILD_PROJECT_NAME", ""
)


def snake_to_camel(snake_str):
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def is_running_on_lambda():
    return "AWS_EXECUTION_ENV" in os.environ


def get_bedrock_client(region=BEDROCK_REGION):
    client = boto3.client("bedrock", region_name=region)
    return client


def get_bedrock_runtime_client(region=BEDROCK_REGION):
    client = boto3.client("bedrock-runtime", region_name=region)
    return client


def get_bedrock_agent_client(region=BEDROCK_REGION):
    client = boto3.client("bedrock-agent", region_name=region)
    return client


def get_bedrock_agent_runtime_client(region=BEDROCK_REGION):
    client = boto3.client("bedrock-agent-runtime", region_name=region)
    return client


def get_current_time():
    # Get current time as milliseconds epoch time
    return int(datetime.now().timestamp() * 1000)


def generate_presigned_url(
    bucket: str,
    key: str,
    content_type: str | None = None,
    expiration=3600,
    client_method: Literal["put_object", "get_object"] = "put_object",
) -> str:
    # See: https://github.com/boto/boto3/issues/421#issuecomment-1849066655
    client = boto3.client(
        "s3",
        region_name=BEDROCK_REGION,
        config=Config(signature_version="v4", s3={"addressing_style": "path"}),
    )
    params = {"Bucket": bucket, "Key": key}
    if content_type:
        params["ContentType"] = content_type
    response = client.generate_presigned_url(
        ClientMethod=client_method,
        Params=params,
        ExpiresIn=expiration,
        HttpMethod="PUT" if client_method == "put_object" else "GET",
    )

    return response


def compose_upload_temp_s3_prefix(user_id: str, bot_id: str) -> str:
    return f"{user_id}/{bot_id}/_temp/"


def compose_upload_temp_s3_path(user_id: str, bot_id: str, filename: str) -> str:
    """Compose S3 path for temporary files.
    This path is used for uploading files to S3.
    """
    prefix = compose_upload_temp_s3_prefix
    return f"{prefix(user_id, bot_id)}{filename}"


def compose_upload_document_s3_path(user_id: str, bot_id: str, filename: str) -> str:
    """Compose S3 path for documents.
    The files on this path is used for embedding.
    """
    return f"{user_id}/{bot_id}/documents/{filename}"


def delete_file_from_s3(bucket: str, key: str, ignore_not_exist: bool = False):
    client = boto3.client("s3", region_name=BEDROCK_REGION)

    # Check if the file exists
    if not ignore_not_exist:
        try:
            client.head_object(Bucket=bucket, Key=key)
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                raise FileNotFoundError(f"The file does not exist in bucket.")
            else:
                raise

    response = client.delete_object(Bucket=bucket, Key=key)
    return response


def delete_files_with_prefix_from_s3(bucket: str, prefix: str):
    """Delete all objects with the given prefix from the given bucket."""
    client = boto3.client("s3", region_name=BEDROCK_REGION)
    response = client.list_objects_v2(Bucket=bucket, Prefix=prefix)

    if "Contents" not in response:
        return

    for obj in response["Contents"]:
        client.delete_object(Bucket=bucket, Key=obj["Key"])


def check_if_file_exists_in_s3(bucket: str, key: str):
    client = boto3.client("s3", region_name=BEDROCK_REGION)

    # Check if the file exists
    try:
        client.head_object(Bucket=bucket, Key=key)
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False
        else:
            raise

    return True


def move_file_in_s3(bucket: str, key: str, new_key: str):
    client = boto3.client("s3", region_name=BEDROCK_REGION)

    # Check if the file exists
    try:
        client.head_object(Bucket=bucket, Key=key)
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            raise FileNotFoundError(f"The file does not exist in bucket.")
        else:
            raise

    response = client.copy_object(
        Bucket=bucket, Key=new_key, CopySource={"Bucket": bucket, "Key": key}
    )
    response = client.delete_object(Bucket=bucket, Key=key)
    return response


def start_codebuild_project(environment_variables: dict) -> str:
    environment_variables_override = [
        {"name": key, "value": value} for key, value in environment_variables.items()
    ]
    client = boto3.client("codebuild")
    response = client.start_build(
        projectName=PUBLISH_API_CODEBUILD_PROJECT_NAME,
        environmentVariablesOverride=environment_variables_override,
    )
    return response["build"]["id"]
