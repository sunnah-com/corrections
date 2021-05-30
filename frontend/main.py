import requests
import time
from datetime import datetime, timedelta
from extensions import mail
from functools import wraps
from lib.mail import EMail
from pathlib import Path
from werkzeug.exceptions import NotFound
from lib.app import app
from lib.auth import aws_auth
from flask import jsonify, make_response, redirect, render_template, request

LOGOUT_URL = f"https://{app.config['AWS_COGNITO_DOMAIN']}/logout?client_id={app.config['AWS_COGNITO_USER_POOL_CLIENT_ID']}&logout_uri={app.config['AWS_COGNITO_LOGOUT_URL']}"

ALL_QUEUES = app.config["QUEUES"]

def ensure_signin(view):
    @ wraps(view)
    def decorated(*args, **kwargs):
        access_token = request.cookies.get("access_token")
        if access_token == None:
            return redirect("/sign_in")

        return view(access_token, *args, **kwargs)

    return decorated


@ app.route("/", methods=["GET"])
@ ensure_signin
def home(access_token):

    username = request.cookies.get("username")
    return render_template(
        "index.html",
        access_token=access_token,
        username=username,
        LOGOUT_URL=LOGOUT_URL,
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


@app.route("/logout")
def logout():
    response = make_response(redirect("/"))
    response.set_cookie("username", "", expires=0)
    response.set_cookie("access_token", "", expires=0)
    return response


@app.route("/aws_cognito_redirect")
def aws_cognito_redirect():
    access_token = aws_auth.get_access_token(request.args)
    response = make_response(redirect("/"))
    expires = datetime.utcnow() + timedelta(minutes=10)
    aws_auth.token_service.verify(access_token)
    response.set_cookie(
        "username",
        aws_auth.token_service.claims["username"],
        expires=expires,
        httponly=True,
    )
    response.set_cookie("access_token", access_token,
                        expires=expires, httponly=True)
    return response


@app.route("/sign_in")
def sign_in():
    return redirect(aws_auth.get_sign_in_url())


def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    mail.init_app(app)

    return None


def reset_correction(correction):
    # format of id is timestamp:aws_request_id where first part is date and second part is random string
    reset_fields = ["id", "version", "lastAssigned"]
    if "id" in reset_fields:
        aws_request_id = next(iter(correction["id"].split(":", 1)[1:]), "")
        correction["id"] = f"{time.time()}:{aws_request_id}"
    if "version" in reset_fields:
        correction["version"] = 0
    if "lastAssigned" in reset_fields:
        correction.pop("lastAssigned", None)
    return correction


with app.app_context():
    extensions(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
