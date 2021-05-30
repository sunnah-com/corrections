from lib.app import app
from flask_awscognito import AWSCognitoAuthentication

aws_auth = AWSCognitoAuthentication(app)
