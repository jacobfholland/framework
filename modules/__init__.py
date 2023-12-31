from app.log.logger import create_logger

logger = create_logger(__name__)


try:
    logger.debug(f"Importing module: Movie")
    from . import movie
except Exception as e:
    logger.error(f"Failed to import modules: {e}")
