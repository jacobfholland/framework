import logging


def disable_logging(func):
    def wrapper(*args, **kwargs):
        original_log_level = logging.root.level
        try:
            logging.disable(logging.CRITICAL)
            result = func(*args, **kwargs)
        finally:
            logging.disable(original_log_level)
        return result
    return wrapper
