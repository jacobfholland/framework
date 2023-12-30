from app.log.logger import create_logger
logger = create_logger("auth.init")

try:
    from . import movie
    logger.debug(f"Movie model imported")

    # from . import seeds
    # logger.debug(f"Movie seeds imported")
except Exception as e:
    logger.warning(f"Unable to import Movie module")
