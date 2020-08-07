from functools import wraps
import boto3
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, abort, redirect, render_template, make_response
from werkzeug.exceptions import HTTPException
from flask_awscognito import AWSCognitoAuthentication

app = Flask(__name__)
app.config.from_object('config.Config')

aws_auth = AWSCognitoAuthentication(app)


def ensure_signin(view):
    @wraps(view)
    def decorated(*args, **kwargs):
        access_token = request.cookies.get('access_token')
        if access_token == None:
            return redirect('/sign_in')

        return view(access_token, *args, **kwargs)
    return decorated


@app.route('/', methods=['GET'])
@ensure_signin
def home(access_token):

    username = request.cookies.get('username')
    return render_template('index.html', access_token=access_token, username=username)


@app.route('/corrections', methods=['GET'])
@aws_auth.authentication_required
def get_correction():
    dynamodb = boto3.resource('dynamodb',
                              endpoint_url=app.config['DYNAMODB_ENDPOINT_URL'],
                              region_name=app.config['REGION'])
    table = dynamodb.Table(app.config['DYNAMODB_TABLE'])
    response = table.scan(Limit=1)
    return jsonify(response["Items"])


@app.route('/aws_cognito_redirect')
def aws_cognito_redirect():
    access_token = aws_auth.get_access_token(request.args)
    response = make_response(redirect('/'))
    expires = datetime.utcnow() + timedelta(minutes=10)
    aws_auth.token_service.verify(access_token)
    response.set_cookie(
        'username',  aws_auth.token_service.claims["username"], expires=expires, httponly=True)
    response.set_cookie('access_token', access_token,
                        expires=expires, httponly=True)
    return response


@app.route('/sign_in')
def sign_in():
    return redirect(aws_auth.get_sign_in_url())


if __name__ == '__main__':
    app.run(host='0.0.0.0')
