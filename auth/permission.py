from app.log.logger import create_logger
from database.model import Model
from sqlalchemy import Column, Integer, String, Boolean
from .seeds import permission

logger = create_logger(__name__)


class Permission(Model):
    name = Column(String)
    model = Column(String)
    read = Column(Boolean, default=True)
    create = Column(Boolean)
    update = Column(Boolean)
    delete = Column(Boolean)
    # groups relationship

    def seeds(self):
        return permission
