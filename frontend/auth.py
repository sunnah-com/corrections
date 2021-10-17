from datetime import datetime, timedelta
from functools import wraps
from http import HTTPStatus

from flask import Blueprint, abort, make_response, redirect, request
from flask.globals import current_app
from flask.templating import render_template
from flask_awscognito import AWSCognitoAuthentication

from lib.data.user_repository import get_user_repository

auth_blueprint = Blueprint('auth', __name__,
                           template_folder='templates')

ACTION_MANAGE_USERS = "manage_users"
ACTION_VIEW_ARCHIVE = "view_archive"


def aws_auth():
    return AWSCognitoAuthentication(current_app)


def check_action_permission(username, action):
    repository = get_user_repository()
    return repository.check_action_permission(username, action)


def check_queue_permission(username, queue):
    repository = get_user_repository()
    return repository.check_queue_permission(username, queue)


def ensure_queue_permission(username, queue):
    if not check_queue_permission(username, queue):
        abort(HTTPStatus.FORBIDDEN)


def authenticated_api(action=""):
    def decorator(view):
        @wraps(view)
        def decorated(*args, **kwargs):
            username = get_current_user()
            if not username:
                abort(HTTPStatus.UNAUTHORIZED)
            elif action and not check_action_permission(username, action):
                abort(HTTPStatus.FORBIDDEN)
            return view(username, *args, **kwargs)
        return decorated
    return decorator


def authenticated_view(action=""):
    def decorator(view):
        @wraps(view)
        def decorated(*args, **kwargs):
            username = get_current_user()
            if not username:
                return redirect("/sign_in")
            if action and not check_action_permission(username, action):
                return render_template("unauthorized.html"), HTTPStatus.FORBIDDEN
            return view(username, *args, **kwargs)
        return decorated
    return decorator


@auth_blueprint.route("/sign_in")
def sign_in():
    return redirect(aws_auth().get_sign_in_url())


@auth_blueprint.route("/logout")
def logout():
    response = make_response(redirect("/"))
    response.set_cookie("access_token", "", expires=0)
    return response


def get_current_user():
    access_token = request.cookies.get("access_token")
    if not access_token:
        return ""

    auth = aws_auth()
    auth.token_service.verify(access_token)
    username = auth.token_service.claims["username"]
    return username


@auth_blueprint.route("/aws_cognito_redirect")
def aws_cognito_redirect():
    auth = aws_auth()
    access_token = auth.get_access_token(request.args)
    response = make_response(redirect("/"))
    expires = datetime.utcnow() + timedelta(minutes=10)
    response.set_cookie("access_token", access_token,
                        expires=expires, httponly=True)
    return response
