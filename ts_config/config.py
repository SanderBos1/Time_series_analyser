import os 

class Config:
    UPLOAD_FOLDER = 'data/'
    IMAGES_FOLDER = 'static/Images/'
    ALLOWED_EXTENSIONS = {'csv'}
    SECRET_KEY = "98dca8ef6c39030f678e09c5"
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
class DevConfig:
    UPLOAD_FOLDER = 'data/'
    IMAGES_FOLDER = '/ts_app/static/Images/'
    ALLOWED_EXTENSIONS = {'csv'}
    SECRET_KEY = os.urandom(12).hex()
    SESSION_TYPE = "98dca8ef6c39030f678e09c5"
    SESSION_PERMANENT = False
