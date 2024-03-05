from flask import Flask
from flask_migrate import Migrate
from ts_app.ts_config import config
from flask_session import Session
from .login.login import login_bp
from .sidebar_logic.sidebar import sidebar_bp
from .image_creation.image_ts import image_ts_bp
from .ts_decomposition.ts_decomposition import ts_decomposition_bp
from .extensions import db, login
from ts_app.image_creation.python.models import User
import wtforms_json


def create_app():
    app = Flask(__name__)
    app.config.from_object(config.config)
    db.init_app(app)
    migrate = Migrate(app, db)
    login.init_app(app)
    login.login_view = 'login.login'
    wtforms_json.init()


    """ Registering blueprints"""
    app.register_blueprint(login_bp)
    app.register_blueprint(sidebar_bp)
    app.register_blueprint(image_ts_bp)
    app.register_blueprint(ts_decomposition_bp)

    Session(app)
    return app





