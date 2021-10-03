from auth import require_auth
import http
from flask import Blueprint, jsonify
from lib.data.user_repository import get_user_repository
from auth import require_auth

users_api = Blueprint('users_api', __name__,
                      template_folder='templates',
                      url_prefix='/api/users')


@users_api.route("/", methods=["GET"])
@require_auth
def index():
    users = get_user_repository().list()
    for user in users:
        permissions = user["permissions"]
        permissions["actions"] = list(permissions["actions"])
        permissions["queues"] = list(permissions["queues"])

    return jsonify(users)


@ users_api.route("/<string:username>", methods=["POST"])
@ require_auth
def update(username):
    return '', http.HTTPStatus.NO_CONTENT
