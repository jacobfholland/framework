from app.log.logger import create_logger
logger = create_logger("auth.init")

try:
    from . import user
    logger.debug(f"User model imported")

    from . import seeds
    logger.debug(f"Auth seeds imported")
except Exception as e:
    logger.warning(f"Unable to import Auth module")
