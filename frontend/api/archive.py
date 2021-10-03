from flask import Blueprint, jsonify

from auth import require_auth

archive_api = Blueprint('archive_api', __name__,
                        template_folder='templates',
                        url_prefix='/api/archive')


@archive_api.route("/", methods=["GET"])
@require_auth
def index():
    corrections = [
        {
            "collection": "bukhari",
            "hadith": "1",
            "id": "abc"
        },
        {
            "collection": "muslim",
            "hadith": "2",
            "id": "def"
        }]

    return jsonify(corrections)
