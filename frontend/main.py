from pathlib import Path

import requests
from flask import Blueprint, jsonify, current_app, render_template, request
from werkzeug.exceptions import NotFound

from auth import require_auth, ensure_signin

main_blueprint = Blueprint('main', __name__,
                           template_folder='templates')


@ main_blueprint.route("/", methods=["GET"])
@ ensure_signin
def home(access_token):
    logout_url = f"https://{current_app.config['AWS_COGNITO_DOMAIN']}/logout?client_id={current_app.config['AWS_COGNITO_USER_POOL_CLIENT_ID']}&logout_uri={current_app.config['AWS_COGNITO_LOGOUT_URL']}"
    username = request.cookies.get("username")
    return render_template(
        "index.html",
        access_token=access_token,
        username=username,
        logout_url=logout_url,
        queue_name=all_queues()[0],
        email_template=Path('templates/email.html').read_text()
    )


@main_blueprint.route("/users", methods=["GET"])
@ensure_signin
def users(access_token):

    username = request.cookies.get("username")
    return render_template("users.html", access_token=access_token, username=username)


@main_blueprint.route("/archive", methods=["GET"])
@ensure_signin
def archive(access_token):

    username = request.cookies.get("username")
    return render_template("archive.html", access_token=access_token, username=username)


@main_blueprint.route("/api/hadiths/<int:urn>", methods=["GET"])
@require_auth
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


@main_blueprint.route("/api/queues/", methods=["GET"])
@require_auth
def get_queues():
    queues = [{"name": name} for name in all_queues()]
    return jsonify(queues)


def all_queues():
    return current_app.config["QUEUES"]
