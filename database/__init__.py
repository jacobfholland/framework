from app.log.logger import create_logger
import modules
from app import app

from .base import Base
from .database import Database


logger = create_logger("database.init")
logger.warning("Initializing database")
db = Database(Base, "sqlite:///example.db")
app.db = db
logger.debug("Database bound to application")
logger.warning("Database initialization complete")
