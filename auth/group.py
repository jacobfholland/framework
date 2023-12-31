from auth.permission import Permission
from .pivot import permission_group
from app.log.logger import create_logger
from database.model import Model
from sqlalchemy import Column, Integer, String, Boolean
from .seeds import permission
from sqlalchemy.orm import relationship

logger = create_logger(__name__)


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
                "permissions": Permission().get().all()
            }
        ]
