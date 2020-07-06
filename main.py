import functools
import boto3
from flask import Flask, jsonify, request, abort, render_template
from werkzeug.exceptions import HTTPException


app = Flask(__name__)
app.config.from_object('config.Config')


@app.route('/', methods=['GET'])
def home():
    dynamodb = boto3.resource('dynamodb',
                              endpoint_url=app.config['DYNAMODB_ENDPOINT_URL'],
                              region_name=app.config['REGION'])
    table = dynamodb.Table(app.config['DYNAMODB_TABLE'])
    response = table.scan()
    return render_template('index.html', Items = response['Items'])


if __name__ == '__main__':
    app.run(host='0.0.0.0')
