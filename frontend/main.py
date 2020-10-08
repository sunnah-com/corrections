import requests
import boto3
import pymysql.cursors
import time
from datetime import datetime, timedelta
from functools import wraps
from botocore.exceptions import ClientError
from flask import (Flask, jsonify, make_response, redirect, render_template,
                   request)
from flask_awscognito import AWSCognitoAuthentication
from werkzeug.exceptions import NotFound
from extensions import mail
from lib.mail import EMail

app = Flask(__name__)
app.config.from_object('config.Config')

aws_auth = AWSCognitoAuthentication(app)

mysql_properties = {
    "user": app.config['MYSQL_USER'],
    "password": app.config['MYSQL_PASSWORD'],
    "host": app.config['MYSQL_HOST'],
    "db": app.config['MYSQL_DATABASE']
}


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
    return render_template('index.html', access_token=access_token, username=username, queue_name='global')


@app.route('/users', methods=['GET'])
@ensure_signin
def users(access_token):

    username = request.cookies.get('username')
    return render_template('users.html', access_token=access_token, username=username)


@app.route('/corrections/<string:queue_name>', methods=['GET'])
@aws_auth.authentication_required
def get_correction(queue_name):
    dynamodb = boto3.resource('dynamodb',
                              endpoint_url=app.config['DYNAMODB_ENDPOINT_URL'],
                              region_name=app.config['REGION'])
    table = dynamodb.Table(app.config['DYNAMODB_TABLE'])
    response = table.query(
        ExpressionAttributeValues={
            ':v1': queue_name
        },
        KeyConditionExpression="queue = :v1",
        Limit=1)
    correction = next(iter(response["Items"]), None)
    return jsonify(correction)


@app.route('/hadtihs/<int:urn>', methods=['GET'])
@aws_auth.authentication_required
def get_hadith(urn: int):
    response = requests.get(f"https://api.sunnah.com/v1/hadiths/{urn}", headers={
        "Content-Type": "application/json",
        "X-API-KEY": app.config.get("SUNNAH_COM_API_KEY")
    })

    if response.status_code == 200:
        return response.content
    else:
        return NotFound()


@app.route('/corrections/<string:queue_name>/<string:correction_id>', methods=['POST'])
@aws_auth.authentication_required
def resolve_correction(queue_name, correction_id):
    data = request.json
    if 'action' not in data or (data['action'] == 'approve' and 'corrected_value' not in data):
        return jsonify(create_response_message(False, "Please provide valid action param 'reject', 'skip', or 'approve' and 'corrected_value' param"))

    action = data['action']
    username = request.cookies.get('username')

    if action == "reject":
        return archive_correction(queue_name, correction_id, username, None, False)

    elif action == "approve":
        return approve_correction(queue_name, correction_id, username, data['corrected_value'])

    elif action == "skip":
        return skip_correction(queue_name, correction_id, username)

    else:
        return jsonify(create_response_message(False, "Please provide valid action param 'reject', 'skip', or 'approve'"))


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


def approve_correction(queue_name, correction_id, username, corrected_value):
    try:
        response = read_correction(queue_name, correction_id)
        if 'Item' not in response:
            return jsonify(create_response_message(False, "correction with id " + str(correction_id) + " not found"))

        rows_affected = save_correction_to_hadith_table(
            response['Item']['urn'], corrected_value)

        if rows_affected == 1:
            archive_correction(queue_name, correction_id,
                               username, corrected_value, True)
            return jsonify(create_response_message(True, "Successfully updated hadith text"))
        else:
            return jsonify(create_response_message(False, "Failed to update hadith text"))

    except ClientError as e:
        return jsonify(create_response_message(False, e.response['Error']['Message']))
    except pymysql.Error as error:
        return jsonify(create_response_message(False, str(error)))
    except Exception as exception:
        return jsonify(create_response_message(False, "Error - " + str(exception)))


def save_correction_to_hadith_table(urn, corrected_value):
    conn = pymysql.connect(**mysql_properties)
    cursor = conn.cursor()
    query = "UPDATE bukhari_english SET hadithText = %(hadith_text)s WHERE englishURN = %(urn)s;"
    cursor.execute(query, {"hadith_text": corrected_value, "urn": urn})
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected


def get_correction_table():
    dynamodb = boto3.resource('dynamodb',
                              endpoint_url=app.config['DYNAMODB_ENDPOINT_URL'],
                              region_name=app.config['REGION'])
    table = dynamodb.Table(app.config['DYNAMODB_TABLE'])
    return table


def read_correction(queue_name, correction_id):
    return get_correction_table().get_item(Key={'queue': queue_name, 'id': str(correction_id)})


def delete_correction(queue_name, correction_id):
    return get_correction_table().delete_item(Key={'queue': queue_name, 'id': str(correction_id)})


def skip_correction(queue_name, correction_id, username):
    response = read_correction(queue_name, correction_id)
    delete_correction(queue_name, correction_id)
    try:
        # format of id is timestamp:aws_request_id where first part is date and second part is random string
        aws_request_id = next(iter(response['Item']['id'].split(':', 1)[1:]), '')
        response['Item']['id'] = f"{time.time()}:{aws_request_id}"
        get_correction_table().put_item(Item=response['Item'])
        return jsonify(create_response_message(True, "Success"))
    except ClientError as e:
        return jsonify(create_response_message(False, e.response['Error']['Message']))


# Will archive (log) an approved or rejected correction to dynamodb
def archive_correction(queue_name, correction_id, username, corrected_value=None, approved=False):
    dynamodb = boto3.resource('dynamodb',
                              endpoint_url=app.config['DYNAMODB_ENDPOINT_URL'],
                              region_name=app.config['REGION'])
    archive_table = dynamodb.Table(app.config['DYNAMODB_TABLE_ARCHIVE'])
    try:
        response = read_correction(queue_name, correction_id)

        archive_table.put_item(Item={
            'queue': response['Item']['queue'],
            'id': response['Item']['id'],
            'urn': response['Item']['urn'],
            'attr': response['Item']['attr'],
            'val': response['Item']['val'] if not corrected_value else corrected_value,
            'comment': response['Item']['comment'],
            'submittedBy': response['Item']['submittedBy'],
            'modifiedOn': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'modifiedBy': username,
            'approved': approved,
        })
        response = delete_correction(queue_name, correction_id)
    except ClientError as e:
        return jsonify(create_response_message(False, e.response['Error']['Message']))

    return jsonify(create_response_message(True, "Success"))


def create_response_message(success, message):
    return {
        'success': success,
        'message': message
    }


def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    mail.init_app(app)

    return None


with app.app_context():
    extensions(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
