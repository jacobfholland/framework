import logging


try:
    from . import utils, config, log, app
except Exception as e:
    logging.error(f"Failed to import app module: {e}")

try:
    from .log import logger
    logger.critical("Starting application")
    logger.info(f"Core application built successfully")
except Exception as e:
    logging.error(f"Failed to import logger module: {e}")
