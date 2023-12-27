import sys
import os


def create_app(conf, logger):
    try:
        from app.app import Application
        return Application(conf, logger)
    except Exception as e:
        print(f"Failed to import Application class: {e}")
        sys.exit(1)


try:
    from . import utils, config, log
    logger = log.logger
    conf = config.conf
    for k, v in conf.__dict__.items():
        logger.debug(f"{k}: {v}")
    app = create_app(conf, logger)
    logger.info(f"Core application built successfully")
except Exception as e:
    print(f"Failed to build Application: {e}")
    sys.exit(1)
