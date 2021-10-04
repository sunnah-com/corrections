import requests
from auth import require_auth
from flask import Blueprint, current_app, jsonify
from lib.utils import all_queues
from werkzeug.exceptions import NotFound

misc_api = Blueprint('misc_api', __name__,
                     template_folder='templates',
                     url_prefix='/api')


@misc_api.route("/queues/", methods=["GET"])
@require_auth()
def get_queues():
    queues = [{"name": name} for name in all_queues()]
    return jsonify(queues)


@misc_api.route("/hadiths/<int:urn>", methods=["GET"])
@require_auth()
def get_hadith(urn: int):
    response = requests.get(
        f"https://api.sunnah.com/v1/hadiths/{urn}",
        headers={
            "Content-Type": "application/json",
            "X-API-KEY": current_app.config.get("SUNNAH_COM_API_KEY"),
        },
    )

    if response.status_code == 200:
        return response.content
    else:
        return NotFound()
