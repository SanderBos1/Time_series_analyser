from flask import Flask
from ts_config import config
from ts_python import *

app = Flask(__name__)
app.config.from_object(config.Config)

from ts_app import routes
