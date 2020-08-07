from functools import wraps
import boto3
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, abort, redirect, render_template, make_response
from werkzeug.exceptions import HTTPException
from flask_awscognito import AWSCognitoAuthentication
from botocore.exceptions import ClientError
import pymysql.cursors
from datetime import datetime

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

@app.route('/corrections/<int:correction_id>', methods=['POST'])
@aws_auth.authentication_required
def resolve_correction(correction_id):
    req_data = request.form
    if 'action' not in req_data and 'corrected_hadith' not in req_data:
        return jsonify(create_response_message("Please provide valid action param 'delete' or 'approve' and 'corrected_hadith' param"))

    action = req_data['action']
    corrected_hadith = req_data['corrected_hadith']
    username = request.cookies.get('username')

    if action == "delete":
        return archive_correction(correction_id, username, None, False)

    elif action == "approve":
        dynamodb = boto3.resource('dynamodb',
            endpoint_url=app.config['DYNAMODB_ENDPOINT_URL'],
            region_name=app.config['REGION'])
        table = dynamodb.Table(app.config['DYNAMODB_TABLE'])
        try:
            response = table.get_item(Key={'id': str(correction_id)})
            if 'Item' not in response:
                return jsonify(create_response_message("correction with id " + str(correction_id) + " not found"))
 
            rows_affected = save_correction_to_hadith_table(response['Item']['urn'], corrected_hadith)

            if rows_affected == 1:
                archive_correction(correction_id, username, corrected_hadith, True)
                return jsonify(create_response_message("Successfully updated hadith text"))
            else:
                return jsonify(create_response_message("Failed to update hadith text"))

        except ClientError as e:
            print(e)
            return jsonify(create_response_message(e.response['Error']['Message']))
        except pymysql.Error as error:
            print(error)
            return jsonify(create_response_message(str(error)))
        except Exception as exception:
            return jsonify(create_response_message("Error - " + str(exception)))

    else:
        return jsonify(create_response_message("Please provide valid action param 'delete' or 'approve'"))

@app.route('/sign_in')
def sign_in():
    return redirect(aws_auth.get_sign_in_url())

def save_correction_to_hadith_table(urn, corrected_hadith):
    conn = pymysql.connect(**mysql_properties)
    cursor = conn.cursor()
    query = "UPDATE bukhari_english SET hadithText = %(hadith_text)s WHERE englishURN = %(urn)s;"
    cursor.execute(query, { "hadith_text": corrected_hadith, "urn": urn })
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected

# Will archive (log) an approved or deleted correction to dynamodb
def archive_correction(correction_id, username, corrected_hadith=None, approved=False):
    dynamodb = boto3.resource('dynamodb',
                endpoint_url=app.config['DYNAMODB_ENDPOINT_URL'],
                region_name=app.config['REGION'])
    table = dynamodb.Table(app.config['DYNAMODB_TABLE'])
    archive_table = dynamodb.Table(app.config['DYNAMODB_TABLE_ARCHIVE'])
    try:
        response = table.get_item(Key={'id': str(correction_id)})
        archive_response = archive_table.put_item(Item={
            'id': response['Item']['id'],
            'urn': response['Item']['urn'],
            'attr': response['Item']['attr'],
            'val': response['Item']['val'] if not corrected_hadith else corrected_hadith,
            'comment': response['Item']['comment'],
            'submittedBy': response['Item']['submittedBy'],
            'modifiedOn': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'modifiedBy': username,
            'approved': approved,
        })
        response = table.delete_item(Key={'id': str(correction_id)})
    except ClientError as e:
        return jsonify(create_response_message(e.response['Error']['Message']))

    return jsonify(create_response_message("Success"))

def create_response_message(message):
    return { 'message': message }

if __name__ == '__main__':
    app.run(host='0.0.0.0')
