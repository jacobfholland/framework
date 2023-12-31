from database.model import Model
from bcrypt import checkpw, gensalt, hashpw
from sqlalchemy import Column, Integer, String

from app.log.logger import create_logger
from .seeds import system

logger = create_logger(__name__)


class User(Model):
    _name = "auth.user"
    name = Column(String)
    username = Column(String)
    password = Column(String)
    avatar = Column(String)

    def seeds(self):
        return system

    def create_not_exists(self, **values):
        del values["password"]
        return super().create_not_exists(**values)

    def create(self, **values):
        # Hash the password
        super().create(**values)
