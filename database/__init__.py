import modules
from app import app

from .base import Base
from .database import Database
from .logger import logger

db = Database(Base, "sqlite:///example.db")

app.db = db
logger.debug("Database bound to application")
