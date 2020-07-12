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
    AWS_DEFAULT_REGION = REGION
    AWS_COGNITO_DOMAIN = 'sunnah.auth.us-west-2.amazoncognito.com'
    AWS_COGNITO_USER_POOL_ID = 'us-west-2_VwNXYJUAS'
    AWS_COGNITO_USER_POOL_CLIENT_ID = '5hsoggtqnoh3u78urbt77iuni8'
    AWS_COGNITO_USER_POOL_CLIENT_SECRET = '8v5bj6d5ng6p9kfocnp6b4puv935dt6u22aj3mvaao66u2grufs'
    AWS_COGNITO_REDIRECT_URL = 'http://localhost:5000/aws_cognito_redirect'
