import boto3
import pytest


from config import Config


@pytest.fixture
def dynamodb():
    return boto3.resource(
        "dynamodb",
        endpoint_url=Config.DYNAMODB_ENDPOINT_URL,
        region_name=Config.REGION,
    )
