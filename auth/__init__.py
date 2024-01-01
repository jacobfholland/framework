from app.log.logger import create_logger

logger = create_logger(__name__)

try:
    logger.debug(f"Importing module components: Auth")
    from . import group, permission, pivot, user
except Exception as e:
    logger.warning(f"Failed to import module: Auth - {e}")
