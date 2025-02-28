import os
import logging
from config import Config

# Logging configuration
log_file_path = os.path.join(Config.LOG_PATH, 'backend.log')
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

# Create a custom logger
logger = logging.getLogger()
logger.setLevel(Config.LOGGING_LEVEL)

# Create handlers
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(Config.LOGGING_LEVEL)

console_handler = logging.StreamHandler()
console_handler.setLevel(Config.LOGGING_LEVEL)

# Create formatter and add it to handlers
formatter = logging.Formatter(Config.LOGGING_FORMAT)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)