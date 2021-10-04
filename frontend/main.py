from pathlib import Path

from flask import Blueprint, current_app, render_template

from auth import ensure_signin, ACTION_MANAGE_USERS, ACTION_VIEW_ARCHIVE
from lib.utils import all_queues

main = Blueprint('main', __name__,
                 template_folder='templates')


@main.route("/", methods=["GET"])
@ensure_signin()
def home(username):
    logout_url = f"https://{current_app.config['AWS_COGNITO_DOMAIN']}/logout?client_id={current_app.config['AWS_COGNITO_USER_POOL_CLIENT_ID']}&logout_uri={current_app.config['AWS_COGNITO_LOGOUT_URL']}"
    return render_template(
        "index.html",
        username=username,
        logout_url=logout_url,
        queue_name=all_queues()[0],
        email_template=Path('templates/email.html').read_text()
    )


@main.route("/users", methods=["GET"])
@ensure_signin(action=ACTION_MANAGE_USERS)
def users(username):
    return render_template("users.html", username=username)


@main.route("/archive", methods=["GET"])
@ensure_signin(action=ACTION_VIEW_ARCHIVE)
def archive(username):
    return render_template("archive.html", username=username)
