from extensions import mail
from flask import Flask

app = Flask(__name__, static_folder='../static',
            template_folder='../templates')
app.config.from_object("config.Config")

from lib.corrections import corrections_blueprint
app.register_blueprint(corrections_blueprint)

from lib.auth import auth_blueprint
app.register_blueprint(auth_blueprint)


def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    mail.init_app(app)

    return None


with app.app_context():
    extensions(app)
