import os
import logging

class Config:
    ENV = os.environ.get('ENV', 'prod')
    LOGGING_LEVEL = logging.INFO if ENV == 'dev' else logging.WARN
    LOGGING_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/app/upload')
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024  # 1 MB
