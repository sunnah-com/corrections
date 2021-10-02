import os
from dotenv import load_dotenv

load_dotenv(".env.local")


class Config(object):
    JSON_SORT_KEYS = False
    DYNAMODB_ENDPOINT_URL = os.environ.get("DYNAMODB_ENDPOINT_URL")
    DYNAMODB_TABLE = os.environ.get("DYNAMODB_TABLE")
    DYNAMODB_TABLE_ARCHIVE = os.environ.get("DYNAMODB_TABLE_ARCHIVE")

    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    REGION = os.environ.get("REGION")

    AWS_DEFAULT_REGION = REGION
    AWS_COGNITO_DOMAIN = os.environ.get("AWS_COGNITO_DOMAIN")
    AWS_COGNITO_USER_POOL_ID = os.environ.get("AWS_COGNITO_USER_POOL_ID")
    AWS_COGNITO_USER_POOL_CLIENT_ID = os.environ.get(
        "AWS_COGNITO_USER_POOL_CLIENT_ID")
    AWS_COGNITO_USER_POOL_CLIENT_SECRET = os.environ.get(
        "AWS_COGNITO_USER_POOL_CLIENT_SECRET"
    )
    AWS_COGNITO_REDIRECT_URL = os.environ.get("AWS_COGNITO_REDIRECT_URL")
    AWS_COGNITO_LOGOUT_URL = os.environ.get("AWS_COGNITO_LOGOUT_URL")

    MYSQL_USER = os.environ.get("MYSQL_USER")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
    MYSQL_HOST = os.environ.get("MYSQL_HOST")
    MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE")

    SUNNAH_COM_API_KEY = os.environ.get("SUNNAH_COM_API_KEY")

    # Flask Mail
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    # Queues
    QUEUES = os.environ.get("QUEUES").split(",")
