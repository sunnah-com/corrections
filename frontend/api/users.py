from http import HTTPStatus

from auth import ACTION_MANAGE_USERS, authenticated_api
from flask import Blueprint, jsonify
from lib.data.user_repository import get_user_repository

users_api = Blueprint('users_api', __name__,
                      template_folder='templates',
                      url_prefix='/api/users')


@users_api.route("/", methods=["GET"])
@authenticated_api(action=ACTION_MANAGE_USERS)
def index(username):
    users = get_user_repository().list()
    for user in users:
        permissions = user["permissions"]
        permissions["actions"] = list(permissions["actions"])
        permissions["queues"] = list(permissions["queues"])

    return jsonify(users)


@ users_api.route("/<string:username>", methods=["POST"])
@ authenticated_api(action=ACTION_MANAGE_USERS)
def update(username):
    return '', HTTPStatus.NO_CONTENT
