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
import json
from sqlalchemy.orm import Session
from app.utils.validate import validate_model
from sqlalchemy.orm.decl_api import registry
from app.log.logger import create_logger

logger = create_logger(__name__)

IGNORE_KEYS = [
    "wsgi.input",
    "wsgi.errors",
    "werkzeug.socket",
    "werkzeug.request"
]
"""List of keys to be ignored during the serialization process."""


def delete_value(data: dict[Any], key: str) -> None:
    """Delete a specific key-value pair from a dictionary.

    Attempts to remove a key from the dictionary's `environ` key.

    Notes:
        - The function is primarily used during the serilization of Werkzeug's 
          Request object. 

    Args:
        - ``data`` (dict[Any]): The dictionary from which the key-value pair will 
          be deleted. 
        - ``key`` (str): The key that needs to be deleted. 

    Raises:
        - ``KeyError``: If the value doesn't exist gracefully ignore it. 
    """

    try:
        del data["environ"][key]
    except KeyError as e:
        logger.debug(f"Key {key} not found on object during serilization")
        pass


def delete_ignored(data: dict[Any]) -> None:
    """Delete ignored keys from the dictionary.

    Args:
        - ``data`` (dict[Any]): The dictionary from which the ignored keys will be 
          deleted.

    Raises:
        - ``KeyError``: If the value doesn't exist gracefully ignore it.

    Returns:
        ``None``: Void.
    """

    try:
        del data["stream"]
    except KeyError as e:
        pass
    for key in IGNORE_KEYS:
        delete_value(data, key)


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
            data = obj.__getattribute__(field)
            try:
                fields[field] = serialize(data)  # recursively call serialize
            except TypeError:
                fields[field] = str(data)
        return fields
    if isinstance(obj, registry):
        return None
    raise TypeError(f"Unserializable object {obj} of type {type(obj)}")


def process_request(obj: Request) -> dict:
    """Process a Werkzeug Request object and return a serialized dictionary 
    representation.

    Takes a Werkzeug Request object and processes it into a dictionary suitable 
    for serialization. It binds various parts of the request to the dictionary, 
    deletes ignored keys, and sorts the keys in the dictionary.

    Args:
        - ``obj`` (``Request``): The Werkzeug Request object to be processed.

    Returns:
        ``dict``: A dictionary representation of the processed request.
    """

    data = vars(obj)
    bind_args(data, obj)
    bind_json(data, obj)
    bind_form(data, obj)
    delete_ignored(data)
    sort_response(data)
    return data


def bind_form(data: dict[Any], obj: Request) -> None:
    """Bind form data to the dictionary.

    Args:
        - ``data`` (dict[Any]): The dictionary to which the form data will be bound.
        - ``obj`` (``Request``): The Werkzeug Request object.

    Raises:
        - ``KeyError``: If the value doesn't exist gracefully ignore it.

    Returns:
        ``None``: Void.
    """

    try:
        data["form"] = obj.form.to_dict()
    except UnsupportedMediaType as e:
        data["form"] = {}
    except KeyError as e:
        data["form"] = {}
        pass
    except Exception as e:
        data["form"] = {}
        pass


def bind_args(data: dict[Any], obj: Request) -> None:
    """Bind arguments to the dictionary.

    Args:
        - ``data`` (dict[Any]): The dictionary to which the arguments will be bound.
        - ``obj`` (``Request``): The Werkzeug Request object.

    Raises:
        - ``KeyError``: If the value doesn't exist gracefully ignore it.

    Returns:
        ``None``: Void.
    """

    try:
        data["args"] = obj.args
    except UnsupportedMediaType as e:
        data["args"] = {}
    except KeyError as e:
        data["args"] = {}
        pass
    except Exception as e:
        data["args"] = {}
        pass


def bind_json(data: dict[Any], obj: Request) -> None:
    """Bind JSON data to the dictionary.

    Args:
        - ``data`` (dict[Any]): The dictionary to which the JSON data will be bound.
        - ``obj`` (``Request``): The Werkzeug Request object.

    Raises:
        - ``KeyError``: If the value doesn't exist gracefully ignore it.

    Returns:
        ``None``: Void.
    """

    try:
        data["json"] = obj.json
    except UnsupportedMediaType as e:
        data["json"] = {}
    except KeyError as e:
        data["json"] = {}
        pass
    except Exception as e:
        data["json"] = {}
        pass


def sort_response(data: dict[Any]) -> None:
    """Sort dictionary keys and relocate the 'files' key.

    Args:
        - ``data`` (dict[Any]): The dictionary that needs sorting.

    Returns:
        ``None``: Void.
    """

    data = {
        k: data[k]
        for k in sorted(data)
        if not k.lower().startswith("_")
    }
    files_value = data.pop("files")
    data["files"] = files_value
