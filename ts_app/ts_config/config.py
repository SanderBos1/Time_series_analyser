from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    UPLOAD_FOLDER = 'data/'
    ALLOWED_EXTENSIONS = {'csv'}
    SECRET_KEY = os.getenv('SECRET_KEY')
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/Time_series"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig:
    UPLOAD_FOLDER = 'data/'
    ALLOWED_EXTENSIONS = {'csv'}
    SECRET_KEY = os.getenv('SECRET_KEY')    
    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = False
    SESSION_PERMANENT = False
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/Time_series"
