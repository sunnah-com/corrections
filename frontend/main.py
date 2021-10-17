from pathlib import Path

from flask import Blueprint, current_app, render_template

from auth import authenticated_view, ACTION_MANAGE_USERS, ACTION_VIEW_ARCHIVE
from lib.utils import all_queues

main = Blueprint('main', __name__,
                 template_folder='templates')


@main.route("/", methods=["GET"])
@authenticated_view()
def home(username):
    return render_view(
        "index.html",
        username,
        queue_name=next(iter(all_queues(username)), ""),
        email_template=Path('templates/email.html').read_text()
    )


@main.route("/users", methods=["GET"])
@authenticated_view(action=ACTION_MANAGE_USERS)
def users(username):
    return render_view("users.html", username)


@main.route("/archive", methods=["GET"])
@authenticated_view(action=ACTION_VIEW_ARCHIVE)
def archive(username):
    return render_view("archive.html", username)


def render_view(template_name, username, **context):
    logout_url = f"https://{current_app.config['AWS_COGNITO_DOMAIN']}/logout?client_id={current_app.config['AWS_COGNITO_USER_POOL_CLIENT_ID']}&logout_uri={current_app.config['AWS_COGNITO_LOGOUT_URL']}"

    return render_template(template_name,
                           username=username,
                           logout_url=logout_url,
                           **context)
