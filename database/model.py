from datetime import datetime

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
            active = Column(Boolean, default=True)

            @declared_attr
            def __tablename__(cls) -> str:
                return snake_case(cls.__name__)

            def __init__(self, **kwargs):
                for kwarg in kwargs:
                    if hasattr(self, kwarg):
                        setattr(self, kwarg, kwargs[kwarg])
except Exception as e:
    logger.warning("Unable to import base model")
