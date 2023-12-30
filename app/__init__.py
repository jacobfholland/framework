from . import config, log, utils
import logging
import os
import sys


def create_app():
    try:
        from app.app import Application
        return Application()
    except Exception as e:
        logging.error(f"Failed to build application: {e}")
        sys.exit(1)


# try:
logger = log.logger

app = create_app()
logger.info(f"Core application built successfully")
# except Exception as e:
