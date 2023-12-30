from bcrypt import checkpw, gensalt, hashpw
from sqlalchemy import Column, Integer, String

from app import app
from app.log.logger import create_logger

logger = create_logger("auth.user")


try:
    if app.conf.DATABASE and app.conf.AUTH:
        from database.model import Model

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

        logger.debug(f"User model imported")
except Exception as e:
    logger.warning(f"Unable to import model User")
