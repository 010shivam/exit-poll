from flask import Flask
from .db import init_db
from config import Config
def create_app():
    app = Flask(__name__, template_folder="../templates")
    init_db()
    app.config.from_object("config.Config")
    app.secret_key = Config.APP_SECRET_KEY
    from .routes import main
    app.register_blueprint(main)

    return app