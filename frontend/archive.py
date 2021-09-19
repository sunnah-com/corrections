from flask import Blueprint, jsonify

from auth import aws_auth

archive_blueprint = Blueprint('archive', __name__,
                              template_folder='templates',
                              url_prefix='/api/archive')


@archive_blueprint.route("/", methods=["GET"])
@aws_auth.authentication_required
def list():
    corrections = []

    return jsonify(corrections)
