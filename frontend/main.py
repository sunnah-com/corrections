from pathlib import Path

import requests
from flask import jsonify, render_template, request
from werkzeug.exceptions import NotFound

from lib.app import app
from lib.auth import aws_auth, ensure_signin

LOGOUT_URL = f"https://{app.config['AWS_COGNITO_DOMAIN']}/logout?client_id={app.config['AWS_COGNITO_USER_POOL_CLIENT_ID']}&logout_uri={app.config['AWS_COGNITO_LOGOUT_URL']}"

ALL_QUEUES = app.config["QUEUES"]


@ app.route("/", methods=["GET"])
@ ensure_signin
def home(access_token):

    username = request.cookies.get("username")
    return render_template(
        "index.html",
        access_token=access_token,
        username=username,
        logout_url=LOGOUT_URL,
        queue_name=ALL_QUEUES[0],
        email_template=Path('templates/email.html').read_text()
    )


@app.route("/users", methods=["GET"])
@ensure_signin
def users(access_token):

    username = request.cookies.get("username")
    return render_template("users.html", access_token=access_token, username=username)


@app.route("/archive", methods=["GET"])
@ensure_signin
def archive(access_token):

    username = request.cookies.get("username")
    return render_template("archive.html", access_token=access_token, username=username)


@app.route("/hadiths/<int:urn>", methods=["GET"])
@aws_auth.authentication_required
def get_hadith(urn: int):
    response = requests.get(
        f"https://api.sunnah.com/v1/hadiths/{urn}",
        headers={
            "Content-Type": "application/json",
            "X-API-KEY": app.config.get("SUNNAH_COM_API_KEY"),
        },
    )

    if response.status_code == 200:
        return response.content
    else:
        return NotFound()


@app.route("/queues/", methods=["GET"])
@aws_auth.authentication_required
def get_queues():
    queues = [{"name": name} for name in ALL_QUEUES]
    return jsonify(queues)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
