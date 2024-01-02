import base64
from datetime import date, datetime, time
import json

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.inspection import inspect

from app.log.logger import create_logger
from app.utils.bind import bind_values
from app.utils.format import snake_case
from app.utils.generate import generate_uuid
from app.utils.json import serialize
from app.utils.printable import Printable
from app.utils.validate import validate_model
from sqlalchemy_serializer import SerializerMixin
from .base import Base
from .crud import Crud
from .seed import Seed
from werkzeug.datastructures import EnvironHeaders
from werkzeug.datastructures.file_storage import FileStorage
logger = create_logger(__name__)

try:

    class Model(Base, SerializerMixin, Crud, Seed, Printable):
        __table_args__ = {'extend_existing': True}
        __abstract__ = True
        _name = __name__
        _seed_key = None
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
            bind_values(self, kwargs)

        def get_relationship_names(self):
            """Get a list of relationship attribute names for the model."""
            mapper = inspect(self.__class__)
            return [rel.key for rel in mapper.relationships]


except Exception as e:
    logger.warning(f"Unable to import base model: {e}")
