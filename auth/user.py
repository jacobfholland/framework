from database.model import Model
from bcrypt import checkpw, gensalt, hashpw
from sqlalchemy import Column, Integer, String

from app.log.logger import create_logger

logger = create_logger(__name__)


class User(Model):
    name = Column(String)
    username = Column(String)
    password = Column(String)
    avatar = Column(String)

    def seeds(self):
        from .seeds import system
        return system

    def create_not_exists(self, **values):
        del values["password"]
        return super().create_not_exists(**values)

    def create(self, **values):
        # Hash the password
        super().create(**values)
