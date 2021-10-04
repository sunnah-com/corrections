from datetime import datetime, timedelta
from functools import wraps
from http import HTTPStatus

from flask import Blueprint, make_response, redirect, request, abort
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


def check_user_permission(action):
    username = request.cookies.get("username")
    return username and get_user_repository().check_permission(username, action)


def require_auth(action=""):
    def decorator(view):
        @wraps(view)
        def decorated(*args, **kwargs):
            if action and not check_user_permission(action):
                abort(HTTPStatus.UNAUTHORIZED)

            authenticated_view = aws_auth().authentication_required(view)
            return authenticated_view(*args, **kwargs)
        return decorated
    return decorator


def ensure_signin(action=""):
    def decorator(view):
        @wraps(view)
        def decorated(*args, **kwargs):
            access_token = request.cookies.get("access_token")
            if access_token == None:
                return redirect("/sign_in")
            if action and not check_user_permission(action):
                return redirect("/unauthorized")
            return view(access_token, *args, **kwargs)
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
    response.set_cookie("username", "", expires=0)
    response.set_cookie("access_token", "", expires=0)
    return response


@auth_blueprint.route("/aws_cognito_redirect")
def aws_cognito_redirect():
    auth = aws_auth()
    access_token = auth.get_access_token(request.args)
    auth.token_service.verify(access_token)

    response = make_response(redirect("/"))
    expires = datetime.utcnow() + timedelta(minutes=10)
    response.set_cookie(
        "username",
        auth.token_service.claims["username"],
        expires=expires,
        httponly=True,
    )
    response.set_cookie("access_token", access_token,
                        expires=expires, httponly=True)
    return response
