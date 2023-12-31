from datetime import datetime, date

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declared_attr

from app.log.logger import create_logger
from app.utils.format import snake_case
from app.utils.generate import generate_uuid
from app.utils.printable import Printable
from app.utils.validate import validate_model
from sqlalchemy.inspection import inspect

from .base import Base
from .crud import Crud
from .seed import Seed


logger = create_logger(__name__)

try:

    class Model(Base, Crud, Seed, Printable):
        __table_args__ = {'extend_existing': True}
        __abstract__ = True
        _name = __name__
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
            self.update_values(kwargs)

        def get_relationship_names(self):
            """Get a list of relationship attribute names for the model."""
            mapper = inspect(self.__class__)
            return [rel.key for rel in mapper.relationships]

        def update_values(self, values):
            data = {**self.__dict__, **values}
            for key, value in data.items():
                if hasattr(self, key):
                    setattr(self, key, value)
                else:
                    logger.warning(
                        f"Key {key} does not exist on {self.__class__.__name__} model")

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
