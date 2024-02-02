from flask import Flask
from ts_config import config
from ts_python import *
from flask_session import Session

app = Flask(__name__)
app.config.from_object(config.DevConfig)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
from ts_app import routes
