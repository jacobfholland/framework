from datetime import datetime, date

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declared_attr

from app import app
from app.log.logger import create_logger
from app.utils.format import snake_case
from app.utils.generate import generate_uuid

from .base import Base


logger = create_logger("database.model")

try:
    if app.conf.DATABASE:
        from .crud import Crud
        from .seed import Seed

        class Model(Base, Crud, Seed):
            __table_args__ = {'extend_existing': True}
            __abstract__ = True

            id = Column(Integer, primary_key=True)
            uuid = Column(String, default=generate_uuid)
            created_at = Column(
                DateTime,
                default=datetime.utcnow,
                doc="Timestamp of creation."
            )
            updated_at = Column(
                DateTime,
                default=datetime.utcnow,
                onupdate=datetime.utcnow,
                doc="Timestamp of the last update."
            )
            deleted_at = Column(
                DateTime,
                doc="Timestamp of deletion."
            )

            @declared_attr
            def __tablename__(cls) -> str:
                return snake_case(cls.__name__)

            def __init__(self, **kwargs):
                for kwarg in kwargs:
                    if hasattr(self, kwarg):
                        setattr(self, kwarg, kwargs[kwarg])
                    else:
                        logger.warning(
                            f"Key {kwarg} does not exist on {self.__class__.__name__} model")

            def serialize(self):
                serialized_data = {}
                for column in self.__table__.columns:
                    attribute = getattr(self, column.name)
                    if isinstance(attribute, (datetime, date)):
                        serialized_data[column.name] = attribute.isoformat()
                    else:
                        serialized_data[column.name] = attribute
                return serialized_data


except Exception as e:
    logger.warning(f"Unable to import base model: {e}")
