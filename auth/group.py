from app.log.logger import create_logger
from database.model import Model
from sqlalchemy import Column, Integer, String, Boolean
from .seeds import permission

logger = create_logger(__name__)


class Group(Model):
    name = Column(String)
    # permissions relationship
