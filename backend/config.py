import os
import logging

class Config:
    ENV = os.environ.get('ENV', 'prod')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/app/upload')

    LOGGING_LEVEL = logging.INFO if ENV == 'dev' else logging.WARN
    LOG_PATH = os.path.join(UPLOAD_FOLDER, 'backend', 'logs') if ENV == 'dev' else '/app/backend/logs'

    LOGGING_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

    MAX_CONTENT_LENGTH = 1 * 1024 * 1024  # 1 MB
