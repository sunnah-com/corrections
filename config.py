import os
from dotenv import load_dotenv

load_dotenv('.env.local')

class Config(object):
    JSON_SORT_KEYS = False
    DYNAMODB_ENDPOINT_URL = '{DYNAMODB_ENDPOINT_URL}'.format(**os.environ)
    DYNAMODB_TABLE = '{DYNAMODB_TABLE}'.format(**os.environ)
    AWS_ACCESS_KEY_ID = '{AWS_ACCESS_KEY_ID}'.format(**os.environ)
    AWS_SECRET_ACCESS_KEY = '{AWS_SECRET_ACCESS_KEY}'.format(**os.environ)
    REGION = '{REGION}'.format(**os.environ)