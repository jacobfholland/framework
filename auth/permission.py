from app.log.logger import create_logger
from database.model import Model
from sqlalchemy import Column, Integer, String, Boolean
# from .seeds import permission
from sqlalchemy.orm import relationship
from .pivot import permission_group
logger = create_logger(__name__)


class Permission(Model):
    name = Column(String)
    model = Column(String)
    read = Column(Boolean, default=True)
    create = Column(Boolean)
    update = Column(Boolean)
    delete = Column(Boolean)
    groups = relationship(
        "Group", secondary=permission_group, back_populates="permissions"
    )

    def seeds(self):
        return [
            {
                "name": "auth.permission",
                "model": "auth.permission",
                "create": True,
                "read": True,
                "update": True,
                "delete": True,
            },
            {
                "name": "auth.group",
                "model": "auth.group",
                "create": True,
                "read": True,
                "update": True,
                "delete": True,
            }
        ]
