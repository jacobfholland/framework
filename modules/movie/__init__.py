from app.log.logger import create_logger
logger = create_logger(__name__)

try:
    logger.debug(f"Importing module components: Movie")
    from . import movie
except Exception as e:
    logger.warning(f"Failed to import module: Movie - {e}")
