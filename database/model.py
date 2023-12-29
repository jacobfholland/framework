from datetime import datetime, date

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declared_attr

from app import app
from app.utils.format import snake_case
from app.utils.generate import generate_uuid

from .base import Base
from .logger import logger

try:
    if app.conf.DATABASE:
        from database.crud import Crud

        class Model(Base, Crud):
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

            def serialize(self):
                serialized_data = {}
                for column in self.__table__.columns:
                    attribute = getattr(self, column.name)
                    # Check if the attribute is a date or datetime and convert to string.
                    if isinstance(attribute, (datetime, date)):
                        serialized_data[column.name] = attribute.isoformat()
                    else:
                        serialized_data[column.name] = attribute
                return serialized_data

            def seed(self):
                seeds = [
                    {
                        "name": "System",
                        "username": "System",
                        "password": "password123"
                    },
                    {
                        "name": "Administrator",
                        "username": "Administrator",
                        "password": "password123"
                    }
                ]
                for seed in seeds:
                    existing = self.get(quiet_log=True, **seed).all()
                    if not existing:
                        record = self.__class__(**seed)
                        record.create(quiet_log=True)


except Exception as e:
    logger.warning("Unable to import base model")
