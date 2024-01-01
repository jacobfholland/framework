from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.log.logger import create_logger
from app.utils.log import disable_logging
from database.model import Model

from .pivot import permission_group

logger = create_logger(__name__)


class Permission(Model):
    _name = "auth.permission"
    _seed_key = "name"
    model = Column(String)
    model_get = Column(Boolean, default=True)
    model_create = Column(Boolean)
    model_update = Column(Boolean)
    model_delete = Column(Boolean)
    groups = relationship(
        "Group", secondary=permission_group, back_populates="permissions"
    )

    def seeds(self):
        return [
            {
                "name": "auth.group",
                "model": "auth.group",
                "model_create": True,
                "model_get": True,
                "model_update": True,
                "model_delete": True,
            },
            {
                "name": "auth.permission",
                "model": "auth.permission",
                "model_create": True,
                "model_get": True,
                "model_update": True,
                "model_delete": True,
            },
            {
                "name": "auth.user",
                "model": "auth.user",
                "model_create": True,
                "model_get": True,
                "model_update": True,
                "model_delete": True,
            }
        ]
