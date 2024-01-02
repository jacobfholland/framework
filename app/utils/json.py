import base64
from datetime import date, datetime, time
from typing import Any, Dict, Union
import types
from werkzeug.datastructures import EnvironHeaders
from werkzeug.datastructures.file_storage import FileStorage
from werkzeug.exceptions import UnsupportedMediaType
from werkzeug.wrappers import Request
from datetime import date, datetime
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Session
from app.utils.validate import validate_model
from sqlalchemy.orm.decl_api import registry
from app.log.logger import create_logger

logger = create_logger(__name__)


def serialize(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, (list, tuple)):
        return [serialize(item) for item in obj]
    if isinstance(obj, dict):
        return {serialize(k): serialize(v) for k, v in obj.items()}
    if callable(obj):
        return
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if hasattr(obj, "__table__"):
        fields = {}
        for field in [
            x
            for x in vars(obj)
            if not x.startswith('_') and x != 'metadata' and not callable(x)
        ]:
            data = getattr(obj, field)
            try:
                fields[field] = serialize(data)
            except TypeError:
                fields[field] = str(data)
        return fields
    if isinstance(obj, registry):
        return None
    raise TypeError(f"Unserializable object {obj} of type {type(obj)}")
