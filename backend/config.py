import os
import logging

class Config:
    LOGGING_LEVEL = logging.ERROR
    LOGGING_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/app/upload')
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024  # 1 MB
