from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.log.logger import create_logger
from app.utils.log import disable_logging

from database.model import Model
from auth.permission import Permission
from .pivot import permission_group


logger = create_logger(__name__)


class Group(Model):
    _name = "auth.group"
    _seed_key = "name"
    name = Column(String)
    permissions = relationship(
        "Permission", secondary=permission_group, back_populates="groups"
    )

    def seeds(self):
        permissions = Permission().get().all()
        return [
            {
                "name": "Bubble222s",
                "permissions": permissions
            }
        ]
