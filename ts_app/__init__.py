from flask import Flask
from ts_app.ts_config import config
from ts_app.ts_python import *
from flask_session import Session
from .login.login import login_bp
from .image_creation.image_ts import image_ts_bp
from .sequencing.sequencing import sequencing_bp
from .granger_causality.granger_causality import granger_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)
    app.register_blueprint(login_bp)
    app.register_blueprint(image_ts_bp)
    app.register_blueprint(sequencing_bp)
    app.register_blueprint(granger_bp)
    Session(app)
    return app


