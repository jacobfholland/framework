import logging

from app.log.level import LOG_LEVEL, LOG_LEVELS


def disable_logging(func):
    def wrapper(*args, **kwargs):
        original_log_level = LOG_LEVELS.get(LOG_LEVEL)
        try:
            logging.disable(logging.CRITICAL)
            result = func(*args, **kwargs)
        finally:
            logging.disable(original_log_level - 10)
        return result
    return wrapper
