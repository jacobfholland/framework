from app.log.logger import create_logger


logger = create_logger("modules.init")


try:
    logger.debug(f"Importing module: Movie")
    from . import movie
    logger.debug(f"Module successfully imported: Movie")
except Exception as e:
    logger.error(f"Failed to import modules")
