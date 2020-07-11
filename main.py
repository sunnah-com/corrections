import functools
import boto3
from flask import Flask, jsonify, request, abort, redirect, render_template
from werkzeug.exceptions import HTTPException
from flask_awscognito import AWSCognitoAuthentication

app = Flask(__name__)
app.config.from_object('config.Config')

aws_auth = AWSCognitoAuthentication(app)

@app.route('/', methods=['GET'])
@aws_auth.authentication_required
def home():
    dynamodb = boto3.resource('dynamodb',
                              endpoint_url=app.config['DYNAMODB_ENDPOINT_URL'],
                              region_name=app.config['REGION'])
    table = dynamodb.Table(app.config['DYNAMODB_TABLE'])
    response = table.scan()
    return render_template('index.html', Items = response['Items'])

@app.route('/aws_cognito_redirect')
def aws_cognito_redirect():
    access_token = aws_auth.get_access_token(request.args)
    return jsonify({'access_token': access_token})

@app.route('/sign_in')
def sign_in():
    return redirect(aws_auth.get_sign_in_url())

if __name__ == '__main__':
    app.run(host='0.0.0.0')
