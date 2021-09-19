from flask import Blueprint, jsonify

from auth import require_auth

archive_blueprint = Blueprint('archive', __name__,
                              template_folder='templates',
                              url_prefix='/api/archive')


@archive_blueprint.route("/", methods=["GET"])
@require_auth
def list():
    corrections = []

    return jsonify(corrections)
