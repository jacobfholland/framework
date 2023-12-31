from app.log.logger import create_logger
logger = create_logger(__name__)

try:
    logger.debug(f"Importing module components: Auth")
    from . import permission, group, user, seeds, pivot
except Exception as e:
    logger.warning(f"Failed to import module: Auth - {e}")
