
class Config:
    UPLOAD_FOLDER = 'data/'
    ALLOWED_EXTENSIONS = {'csv'}
    SECRET_KEY = "98dca8ef6c39030f678e09c5"
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/Time_series"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USER_IMAGE_FOLDER = "Images/"

class DevConfig:
    UPLOAD_FOLDER = 'data/'
    ALLOWED_EXTENSIONS = {'csv'}
    SECRET_KEY = "98dca8ef6c39030f678e09c5"
    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = False
    SESSION_PERMANENT = False
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/Time_series"
    USER_IMAGE_FOLDER = "Images/"
