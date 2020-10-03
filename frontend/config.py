import os
from dotenv import load_dotenv

load_dotenv('.env.local')


class Config(object):
    JSON_SORT_KEYS = False
    DYNAMODB_ENDPOINT_URL = '{DYNAMODB_ENDPOINT_URL}'.format(**os.environ)
    DYNAMODB_TABLE = '{DYNAMODB_TABLE}'.format(**os.environ)
    DYNAMODB_TABLE_ARCHIVE = '{DYNAMODB_TABLE_ARCHIVE}'.format(**os.environ)

    AWS_ACCESS_KEY_ID = '{AWS_ACCESS_KEY_ID}'.format(**os.environ)
    AWS_SECRET_ACCESS_KEY = '{AWS_SECRET_ACCESS_KEY}'.format(**os.environ)
    REGION = '{REGION}'.format(**os.environ)

    AWS_DEFAULT_REGION = REGION
    AWS_COGNITO_DOMAIN = '{AWS_COGNITO_DOMAIN}'.format(**os.environ)
    AWS_COGNITO_USER_POOL_ID = '{AWS_COGNITO_USER_POOL_ID}'.format(**os.environ)
    AWS_COGNITO_USER_POOL_CLIENT_ID = '{AWS_COGNITO_USER_POOL_CLIENT_ID}'.format(**os.environ)
    AWS_COGNITO_USER_POOL_CLIENT_SECRET = '{AWS_COGNITO_USER_POOL_CLIENT_SECRET}'.format(**os.environ)
    AWS_COGNITO_REDIRECT_URL = '{AWS_COGNITO_REDIRECT_URL}'.format(**os.environ)

    MYSQL_USER = '{MYSQL_USER}'.format(**os.environ)
    MYSQL_PASSWORD = '{MYSQL_PASSWORD}'.format(**os.environ)
    MYSQL_HOST = '{MYSQL_HOST}'.format(**os.environ)
    MYSQL_DATABASE = '{MYSQL_DATABASE}'.format(**os.environ)

    SUNNAH_COM_API_KEY = '{SUNNAH_COM_API_KEY}'.format(**os.environ)

    # Flask Mail 
    MAIL_DEAFULT_SENDER = '{MAIL_DEAFULT_SENDER}'.format(**os.environ)
    MAIL_SERVER = '{MAIL_SERVER}'.format(**os.environ)
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = '{MAIL_USERNAME}'.format(**os.environ)
    MAIL_PASSWORD = '{MAIL_PASSWORD}'.format(**os.environ)
