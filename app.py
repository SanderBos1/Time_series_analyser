
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import wtforms_json
from flask_session import Session
from ts_app.ts_config import config


"""
Creates and configures an instance of the Flask application.

Returns:
    The Flask application object.
"""
app = Flask(__name__)
app.config.from_object(config.dev_config)
    
db = SQLAlchemy()
db.init_app(app)
Migrate(app, db)

login = LoginManager()
login.init_app(app)
login.login_view = 'login.login'

wtforms_json.init()

from ts_app.login.login import login_bp
from ts_app.sidebar_logic.sidebar import sidebar_bp
from ts_app.image_creation.image_ts import image_ts_bp
from ts_app.ts_decomposition.ts_decomposition import ts_decomposition_bp

app.register_blueprint(login_bp)
app.register_blueprint(sidebar_bp)
app.register_blueprint(image_ts_bp)
app.register_blueprint(ts_decomposition_bp)

Session(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, threaded=True)