from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.log.logger import create_logger
from app.utils.log import disable_logging
from auth.permission import Permission
from database.model import Model

from .pivot import permission_group
from .seeds import permission

logger = create_logger(__name__)

FULL_CONTROL = {
    "create": True,
    "read": True,
    "update": True,
    "delete": True
}


class Group(Model):

    name = Column(String)
    permissions = relationship(
        "Permission", secondary=permission_group, back_populates="groups"
    )

    def create_not_exists(self, **values):
        return super().create_not_exists(**values)

    def seeds(self):
        return [
            {
                "name": "System",
                "permissions": Permission().get(**FULL_CONTROL).all()
            }
        ]
