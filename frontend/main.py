import functools
import boto3
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, abort, redirect, render_template, make_response
from werkzeug.exceptions import HTTPException
from flask_awscognito import AWSCognitoAuthentication

app = Flask(__name__)
app.config.from_object('config.Config')

aws_auth = AWSCognitoAuthentication(app)

@app.route('/', methods=['GET'])
def home():
    access_token = request.cookies.get('access_token')
    if access_token == None:
        return redirect('/sign_in')
    
    dynamodb = boto3.resource('dynamodb',
                              endpoint_url=app.config['DYNAMODB_ENDPOINT_URL'],
                              region_name=app.config['REGION'])
    table = dynamodb.Table(app.config['DYNAMODB_TABLE'])
    response = table.scan()
    return render_template('index.html', Items = response['Items'], access_token = access_token)

@app.route('/aws_cognito_redirect')
def aws_cognito_redirect():
    access_token = aws_auth.get_access_token(request.args)
    response = make_response(redirect('/'))
    expires = datetime.utcnow() + timedelta(minutes=10)
    response.set_cookie('access_token', access_token, expires=expires)
    return response

@app.route('/sign_in')
def sign_in():
    return redirect(aws_auth.get_sign_in_url())

if __name__ == '__main__':
    app.run(host='0.0.0.0')
