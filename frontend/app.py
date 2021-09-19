from extensions import mail
from flask import Flask


def create_app():
    app = Flask(__name__, static_folder='static',
                template_folder='templates')
    app.config.from_object("config.Config")

    from main import main
    app.register_blueprint(main)

    from api.misc import misc_api
    app.register_blueprint(misc_api)

    from api.corrections import corrections_api
    app.register_blueprint(corrections_api)

    from api.users import users_api
    app.register_blueprint(users_api)

    from api.archive import archive_api
    app.register_blueprint(archive_api)

    from auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    from extensions import mail
    mail.init_app(app)

    return app
