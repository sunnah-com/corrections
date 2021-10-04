from auth import ACTION_VIEW_ARCHIVE, authenticated_api
from flask import Blueprint, jsonify

archive_api = Blueprint('archive_api', __name__,
                        template_folder='templates',
                        url_prefix='/api/archive')


@archive_api.route("/", methods=["GET"])
@authenticated_api(action=ACTION_VIEW_ARCHIVE)
def index(username):
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
