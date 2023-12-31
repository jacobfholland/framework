from app.log import create_logger


logger = create_logger("database.init")


try:
    logger.warning("Initializing database")
    logger.warning("Importing modules")
    import modules
    logger.warning("Modules successfully imported")
except Exception as e:
    logger.error(f"Failed to import modules: {e}")

try:
    logger.warning("Importing module: Auth")
    import auth  # TODO: Make this dynamically import only if the folder exists
    logger.warning(f"Module successfully imported: Auth")
except Exception as e:
    logger.warning(f"Failed to initialize the database: {e}")

try:
    logger.debug(f"Importing module components: Database")
    from . import base, crud, database, model, seed
    logger.debug(f"Module components successfully imported: Database")
    logger.warning("Database initialization completed")
except Exception as e:
    logger.error(f"Failed to initialize the database: {e}")


session = None
