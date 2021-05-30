from flask import Flask

app = Flask(__name__, template_folder='../templates')
app.config.from_object("config.Config")

from lib.corrections import corrections
app.register_blueprint(corrections)
