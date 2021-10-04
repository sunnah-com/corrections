from pathlib import Path

from flask import Blueprint, current_app, render_template, request

from auth import ensure_signin, ACTION_MANAGE_USERS, ACTION_VIEW_ARCHIVE
from lib.utils import all_queues

main = Blueprint('main', __name__,
                 template_folder='templates')


@main.route("/", methods=["GET"])
@ensure_signin()
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


@main.route("/users", methods=["GET"])
@ensure_signin(action=ACTION_MANAGE_USERS)
def users(access_token):

    username = request.cookies.get("username")
    return render_template("users.html", access_token=access_token, username=username)


@main.route("/archive", methods=["GET"])
@ensure_signin(action=ACTION_VIEW_ARCHIVE)
def archive(access_token):

    username = request.cookies.get("username")
    return render_template("archive.html", access_token=access_token, username=username)
