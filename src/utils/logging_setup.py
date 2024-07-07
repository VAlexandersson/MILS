# src/utils/logging_setup.py

import logging
from logging.handlers import RotatingFileHandler
from .config import get_config

def setup_logging():
    config = get_config()
    logger = logging.getLogger('text_splitter')
    logger.setLevel(config.log_level)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(config.log_level)
    console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_format)

    # File handler with rotation
    file_handler = RotatingFileHandler(
        config.log_file,
        maxBytes=config.log_max_size,
        backupCount=config.log_backup_count
    )
    file_handler.setLevel(config.log_level)
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_format)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# Create a global logger instance
logger = setup_logging()