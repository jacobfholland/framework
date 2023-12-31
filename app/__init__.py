import logging

try:
    from . import app, config, log, utils
except Exception as e:
    logging.error(f"Failed to import app module: {e}")

try:
    from .log import logger
    logger.critical("Starting application")
except Exception as e:
    logging.error(f"Failed to import logger module: {e}")
