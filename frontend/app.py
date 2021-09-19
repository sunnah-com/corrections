from extensions import mail
from flask import Flask


def create_app():
    app = Flask(__name__, static_folder='static',
                template_folder='templates')
    app.config.from_object("config.Config")

    from main import main_blueprint
    app.register_blueprint(main_blueprint)

    from corrections import corrections_blueprint
    app.register_blueprint(corrections_blueprint)

    from users import users_blueprint
    app.register_blueprint(users_blueprint)

    from archive import archive_blueprint
    app.register_blueprint(archive_blueprint)

    from auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    from extensions import mail
    mail.init_app(app)

    return app
