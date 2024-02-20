
class Config:
    UPLOAD_FOLDER = 'data/'
    ALLOWED_EXTENSIONS = {'csv'}
    SECRET_KEY = "98dca8ef6c39030f678e09c5"
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/Time_series"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig:
    UPLOAD_FOLDER = 'data/'
    ALLOWED_EXTENSIONS = {'csv'}
    SECRET_KEY = "98dca8ef6c39030f678e09c5"
    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = False
    SESSION_PERMANENT = False
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/Time_series"
