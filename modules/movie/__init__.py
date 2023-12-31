from app.log.logger import create_logger
logger = create_logger("auth.init")

try:
    logger.debug(f"Importing module components: Movie")
    from . import movie
    logger.debug(f"Module components successfully imported: Movie")
except Exception as e:
    logger.warning(f"Failed to import module: Movie")
