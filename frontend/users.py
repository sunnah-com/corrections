import http
from flask import Blueprint, jsonify

from auth import aws_auth

users_blueprint = Blueprint('users', __name__,
                            template_folder='templates',
                            url_prefix='/api/users')


@users_blueprint.route("/", methods=["GET"])
@aws_auth.authentication_required
def list():
    users = [
        {
            "username": "first",
            "permissions": {
                "manage_users": True,
                "view_archive": True,
                "queues": [
                    "global",
                    "secondary"
                ]
            }
        },
        {
            "username": "second",
            "permissions": {
                "manage_users": True,
                "view_archive": False,
                "queues": [
                    "global",
                    "secondary"
                ]
            }
        }
    ]

    return jsonify(users)


@users_blueprint.route("/<string:username>", methods=["POST"])
@aws_auth.authentication_required
def update(username):
    return '', http.HTTPStatus.NO_CONTENT
