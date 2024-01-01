from app.log import create_logger

logger = create_logger(__name__)


try:
    logger.info("Initializing database")
    logger.info("Importing modules")
    import modules
except Exception as e:
    logger.error(f"Failed to import modules: {e}")

try:
    logger.info("Importing module: Auth")
    import auth  # TODO: Make this dynamically import only if the folder exists
except Exception as e:
    logger.warning(f"Failed to import module: Auth - {e}")

try:
    logger.debug(f"Importing module components: Database")
    from . import utils, base, filter, query, crud, database, model, seed
except Exception as e:
    logger.error(f"Failed to initialize the database: {e}")


# session = None
# db = None
