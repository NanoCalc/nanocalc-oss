import os
import logging

class Config:
    # Logger setup
    LOGGING_LEVEL = logging.DEBUG
    LOGGING_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

    # App configuration
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/app/upload')
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024  # 1 MB file size limit

    # Cache configuration
    CACHE_TYPE = 'simple'

    # Database configuration
    SQLALCHEMY_DATABASE_URI  = 'sqlite:///visitors.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

#TODO: check this config
class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    UPLOAD_FOLDER = 'app/upload'