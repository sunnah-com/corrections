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


def check_user_permission(username, action):
    return username and get_user_repository().check_permission(username, action)


def require_auth(action=""):
    def decorator(view):
        @wraps(view)
        def decorated(*args, **kwargs):
            username = get_current_user()
            if not username or (action and not check_user_permission(username, action)):
                abort(HTTPStatus.UNAUTHORIZED)
            return view(username, *args, **kwargs)
        return decorated
    return decorator


def ensure_signin(action=""):
    def decorator(view):
        @wraps(view)
        def decorated(*args, **kwargs):
            username = get_current_user()
            if not username:
                return redirect("/sign_in")
            if action and not check_user_permission(username, action):
                return redirect("/unauthorized")
            return view(username, *args, **kwargs)
        return decorated
    return decorator


@auth_blueprint.route("/sign_in")
def sign_in():
    return redirect(aws_auth().get_sign_in_url())


@auth_blueprint.route("/unauthorized")
def no_permission():
    return render_template("unauthorized.html"), HTTPStatus.UNAUTHORIZED


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
