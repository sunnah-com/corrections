#Importing Modules in Function- Start
from flask import Flask
from main import main
from api.misc import misc_api
from api.corrections import corrections_api
from api.users import users_api
from api.archive import archive_api
from auth import auth_blueprint
from extensions import mail
#Importing Modules in Function- End



def create_app():
    app = Flask(__name__, static_folder='static',
                template_folder='templates')
    app.config.from_object("config.Config")
   
    
    app.register_blueprint(main)
  
    app.register_blueprint(misc_api)
 
    app.register_blueprint(corrections_api)
    
    app.register_blueprint(users_api)
    
    app.register_blueprint(archive_api)
    
    app.register_blueprint(auth_blueprint)
    
    mail.init_app(app)

    return app
