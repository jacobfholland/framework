from app.log.logger import create_logger
logger = create_logger("auth.init")

try:
    logger.debug(f"Importing module components: Auth")
    from . import user
    from . import seeds
    logger.debug(f"Module components successfully imported: Auth")
except Exception as e:
    logger.warning(f"Failed to import module: Auth")
