class Config:
    UPLOAD_FOLDER = 'data/'
    IMAGES_FOLDER = 'static/Images/'
    ALLOWED_EXTENSIONS = {'csv'}
    SECRET_KEY = 'SECRET_KEY'
class DevConfig:
    UPLOAD_FOLDER = 'data/'
    IMAGES_FOLDER = '/ts_app/static/Images/'
    ALLOWED_EXTENSIONS = {'csv'}
    SECRET_KEY = 'SECRET_KEY'