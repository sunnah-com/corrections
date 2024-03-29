import time
from datetime import datetime, timedelta
from decimal import Decimal

import boto3
import pymysql.cursors
from auth import authenticated_api, ensure_queue_permission
from botocore.exceptions import ClientError
from flask import Blueprint, current_app, jsonify, request
from lib.data.archive_item import ArchiveItem
from lib.data.archive_repository import ArchiveRepository
from lib.utils import api_action_response

corrections_api = Blueprint('corrections_api', __name__,
                            template_folder='templates',
                            url_prefix='/api/corrections')


@corrections_api.route("/<string:queue_name>", methods=["GET"])
@authenticated_api()
def get_correction(username, queue_name):
    ensure_queue_permission(username, queue_name)
    table = get_correction_table()

    try_get = True
    start_key = None
    while try_get:
        try_get = False
        expires = datetime.utcnow() - timedelta(minutes=1)
        values = {
            ":q1": queue_name,
            ":t1": Decimal(expires.timestamp()),
            ":v1": 0,
            ":null": None,
        }
        key_condition = "queue = :q1"
        filter = "version = :v1 or lastAssigned = :null or lastAssigned < :t1"
        if start_key:
            response = table.query(
                ExpressionAttributeValues=values,
                KeyConditionExpression=key_condition,
                FilterExpression=filter,
                Limit=1,
                ExclusiveStartKey=start_key,
            )
        else:
            response = table.query(
                ExpressionAttributeValues=values,
                KeyConditionExpression=key_condition,
                FilterExpression=filter,
                Limit=1,
            )
        correction = next(iter(response["Items"]), None)
        if not correction and "LastEvaluatedKey" in response:
            start_key = response["LastEvaluatedKey"]
            try_get = True
        elif correction:
            old_version = correction.get("version", 0)
            correction["version"] = old_version + 1
            now = datetime.utcnow().timestamp()
            try:
                table.update_item(
                    Key={"queue": correction["queue"], "id": correction["id"]},
                    ExpressionAttributeValues={
                        ":v1": old_version,
                        ":v2": correction["version"],
                        ":t1": Decimal(now),
                    },
                    UpdateExpression="SET version = :v2, lastAssigned = :t1",
                    ConditionExpression="version = :v1",
                )
                correction["urn"] = int(correction["urn"])
                correction["version"] = int(correction["version"])
                correction["lastAssigned"] = now
            except ClientError as e:
                if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                    print("Conflict occurred while reserving the item. Trying again...")
                    time.sleep(0.1)
                    try_get = True

    return jsonify(correction)


@corrections_api.route("/<string:queue_name>/<string:correction_id>", methods=["POST"])
@authenticated_api()
def resolve_correction(username, queue_name, correction_id):
    ensure_queue_permission(username, queue_name)

    data = request.json
    valid_action = "action" not in data or (
        data["action"] == "approve" and "corrected_val" not in data
    )
    if valid_action:
        return api_action_response(
            False,
            'Please provide valid action param "reject", "skip", or "approve" and "corrected_val" param',
        )

    action = data["action"]
    email_template = data.get("emailTemplate", "")
    version = data.get("version", 0)

    if action == "reject":
        return reject_correction(
            queue_name, correction_id, email_template, version, username
        )

    elif action == "approve":
        return approve_correction(
            queue_name,
            correction_id,
            email_template,
            version,
            username,
            data["corrected_val"]
        )

    elif action == "skip":
        return skip_correction(queue_name, correction_id, version, username)

    elif action == "move":
        return move_correction(
            queue_name, correction_id, version, data["new_queue_name"]
        )

    else:
        return api_action_response(
            False,
            'Please provide valid action param "reject", "skip", or "approve".',
        )


def reject_correction(queue_name, correction_id, email_template, version, username):
    correction = read_correction(queue_name, correction_id, version)
    if not correction:
        return not_found(correction_id)
    if email_template:
        send_email("rejected", correction, email_template)
    return archive_correction(
        queue_name, correction_id, version, username
    )


def approve_correction(
    queue_name, correction_id, email_template, version, username, corrected_val
):
    try:
        correction = read_correction(queue_name, correction_id, version)
        if not correction:
            return not_found(correction_id)

        attribute = map_hadith_attr(
            correction["attr"]
        )
        if not attribute:
            return invalid_attribute(correction_id)

        rows_affected = save_correction_to_hadith_table(
            correction["urn"], corrected_val, attribute
        )

        if rows_affected > 0:
            archive_correction(
                queue_name,
                correction_id,
                username,
                corrected_val,
                attribute,
                True,
            )

            if email_template:
                send_email("approved", correction,
                           email_template, corrected_val)
            return api_action_response(
                True, "Successfully updated hadith")
        else:
            return api_action_response(False, "Failed to update hadith")

    except ClientError as e:
        return api_action_response(False, e.response["Error"]["Message"])
    except pymysql.Error as error:
        return api_action_response(False, str(error))
    except Exception as exception:
        return api_action_response(False, "Error - " + str(exception))


def map_hadith_attr(attr: str):
    attr_map = {
        "body": "hadithText",
    }
    return attr_map.get(attr, attr)


def get_dynamo_db():
    dynamodb = boto3.resource(
        "dynamodb",
        endpoint_url=current_app.config["DYNAMODB_ENDPOINT_URL"],
        region_name=current_app.config["REGION"],
    )
    return dynamodb


def send_email(
    decision: str,
    correction: dict,
    email_template: str = "",
    corrected_val: str = "",
):
    email = EMail()
    ctx = dict(
        **correction,
        **{"decision": decision, "correctedVal": corrected_val},
    )
    email.send(
        template=email_template,
        ctx=ctx,
        subject=f"Your correction has been {decision}",
        recipients=[correction["submittedBy"]],
    )


def mysql_connect():
    props = {
        "user": current_app.config["MYSQL_USER"],
        "password": current_app.config["MYSQL_PASSWORD"],
        "host": current_app.config["MYSQL_HOST"],
        "db": current_app.config["MYSQL_DATABASE"],
    }
    conn = pymysql.connect(**props)
    return conn


def save_correction_to_hadith_table(urn: int, val: str, attr: str):
    conn = mysql_connect()
    cursor = conn.cursor()
    query = "UPDATE bukhari_english SET {attr} = %(val)s WHERE englishURN = %(urn)s".format(
        attr=attr)
    print(f"Executing {query}, urn={urn}, val={val}")
    cursor.execute(query, {"val": val, "urn": urn})
    rows_affected = cursor.rowcount
    print(f"Affected ", rows_affected, "rows")
    conn.commit()
    conn.close()
    return rows_affected


def get_correction_table():
    return get_dynamo_db().Table(current_app.config["DYNAMODB_TABLE"])


def read_correction(queue_name, correction_id, version):
    response = get_correction_table().get_item(
        Key={"queue": queue_name, "id": str(correction_id)}
    )
    if not ("Item" in response and response["Item"].get("version", 0) == version):
        return None
    return response["Item"]


def delete_correction(queue_name, correction_id, version):
    get_correction_table().delete_item(
        Key={"queue": queue_name, "id": str(correction_id)},
        ExpressionAttributeValues={":v1": version},
        ConditionExpression="version = :v1",
    )


def move_correction(queue_name, correction_id, version, updated_queue_name):
    correction = read_correction(queue_name, correction_id, version)
    if not correction:
        return not_found(correction_id)
    delete_correction(queue_name, correction_id, version)
    try:
        # it is not possible to update an attribute that forms the Key of an item thus we need to copy/delete/put in DynamoDB.
        correction = reset_correction(correction)
        correction["queue"] = updated_queue_name
        get_correction_table().put_item(Item=correction)
        return api_action_response(True, "Successfully moved correction.")
    except Exception as exception:
        return api_action_response(False, "Error - " + str(exception))


def skip_correction(queue_name, correction_id, version, username):
    correction = read_correction(queue_name, correction_id, version)
    if not correction:
        return not_found(correction_id)
    delete_correction(queue_name, correction_id, version)
    try:
        correction = reset_correction(correction)
        get_correction_table().put_item(Item=correction)
        return api_action_response(True, "Successfully skipped correction")
    except ClientError as e:
        return api_action_response(False, e.response["Error"]["Message"])


def archive_correction(
    queue_name: str,
    correction_id: str,
    version: int,
    username: str,
    corrected_val: str = None,
    attribute: str = None,
    approved: bool = False,
):
    archive_repository = ArchiveRepository(
        current_app.config["DYNAMODB_ENDPOINT_URL"],
        current_app.config["REGION"],
        current_app.config["DYNAMODB_TABLE_ARCHIVE"],
    )

    try:
        correction = read_correction(queue_name, correction_id, version)
        if not correction:
            return not_found(correction_id)

        entry = dict(
            **correction,
            **{
                "modifiedBy": username,
                "correctedVal": corrected_val,
                "attribute": attribute,
                "approved": approved,
            },
        )
        archive_repository.write(ArchiveItem.deserialize(entry))
        delete_correction(queue_name, correction_id, version)
    except ClientError as e:
        return api_action_response(False, e.response["Error"]["Message"])

    return api_action_response(True, "Successfully rejected correction")


def reset_correction(correction):
    # format of id is timestamp:aws_request_id where first part is date and second part is random string
    reset_fields = ["id", "version", "lastAssigned"]
    if "id" in reset_fields:
        aws_request_id = next(iter(correction["id"].split(":", 1)[1:]), "")
        correction["id"] = f"{time.time()}:{aws_request_id}"
    if "version" in reset_fields:
        correction["version"] = 0
    if "lastAssigned" in reset_fields:
        correction.pop("lastAssigned", None)
    return correction


def not_found(correction_id):
    return api_action_response(
        False, f'Correction with id "{correction_id}" not found.'
    )


def invalid_attribute(correction_id):
    return api_action_response(
        False, f'Correction with id "{correction_id}" has invalid attribute'
    )
