import logging

from app.config import conf

LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR
}
LOG_LEVEL = conf.LOG_LEVEL.upper()
