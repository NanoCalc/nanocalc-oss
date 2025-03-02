import os
import logging

class Config:
    ENV = os.environ.get('ENV', 'prod')
    LOG_PATH = '/app/logs'
    UPLOAD_FOLDER = '/app/upload'

    LOGGING_LEVEL = logging.INFO if ENV == 'dev' else logging.WARN
    LOGGING_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

    MAX_CONTENT_LENGTH = 1 * 1024 * 1024  # 1 MB
