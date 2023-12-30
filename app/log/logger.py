import logging
import os

import coloredlogs

from app.config import conf
from app.log.format import FORMAT, FORMATTER
from app.log.level import LOG_LEVEL, LOG_LEVELS


def create_logger(name):
    if not os.path.exists(conf.LOG_PATH):
        os.makedirs(conf.LOG_PATH)
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVELS.get(LOG_LEVEL))
    coloredlogs.install(level=LOG_LEVEL, logger=logger, fmt=FORMAT)
    file_handlers = create_handlers(name)
    add_file_handlers(logger, file_handlers)
    return logger


def create_handler(name):
    file_handler = logging.FileHandler(
        f"{conf.LOG_PATH}/{name.lower()}.log")
    file_handler.setLevel(LOG_LEVELS.get(LOG_LEVEL))
    file_handler.setFormatter(FORMATTER)
    return file_handler


def create_handlers(name):
    file_handler = create_handler(name)
    app_file_handler = create_handler("all")
    return [file_handler, app_file_handler]


def add_file_handlers(logger, file_handlers):
    for file_handler in file_handlers:
        logger.addHandler(file_handler)
