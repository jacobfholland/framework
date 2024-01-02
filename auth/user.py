from bcrypt import checkpw, gensalt, hashpw
from sqlalchemy import Column, Integer, String

from app.log.logger import create_logger
from app.utils.log import disable_logging
from database.model import Model
from server.decorator import route


logger = create_logger(__name__)


class User(Model):
    _name = "auth.user"
    _seed_key = "name"
    name = Column(String)
    username = Column(String)
    password = Column(String)
    avatar = Column(String)

    def create(self, **values):
        # Hash the password
        super().create(**values)

    def seeds(self):
        return [
            {
                "name": "System",
                "username": "System",
                "password": "password123",
                "avatar": "/home/jacob/imgs/avatar.jpg"
            },
            {
                "name": "Administrator",
                "username": "Administrator",
                "password": "password123",
                "avatar": "/home/jacob/imgs/avatar.jpg"
            }
        ]

    # @route("/", methods=["GET"], url_prefix="/")
    # def get(cls, request):
    #     records = cls().get().all()
    #     return records
