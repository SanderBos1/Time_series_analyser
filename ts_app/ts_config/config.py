import os
from dotenv import load_dotenv

load_dotenv()


class config:
    UPLOAD_FOLDER = "data/"
    ALLOWED_EXTENSIONS = {"csv"}
    SECRET_KEY = os.getenv("SECRET_KEY")
    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = False
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://postgres:postgres@host.docker.internal:5432/Time_series"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TIME_COLUMN = "Date"


class dev_config:
    UPLOAD_FOLDER = "data/"
    ALLOWED_EXTENSIONS = {"csv"}
    SECRET_KEY = os.getenv("SECRET_KEY")
    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = False
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://postgres:postgres@localhost:5432/Time_series"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TIME_COLUMN = "Date"
