import json


def validate(value):
    for validator in [
        validate_integer, validate_float,
        validate_boolean, validate_json
    ]:
        result, is_valid = validator(value)
        if is_valid:
            return result
    return value


def validate_integer(value):
    try:
        return int(value), True
    except ValueError:
        return None, False


def validate_float(value):
    try:
        return float(value), True
    except ValueError:
        return None, False


def validate_boolean(value):
    if value.lower() in ["true", "false"]:
        return value.lower() == "true", True
    return None, False


def validate_json(value):
    try:
        return json.loads(value), True
    except json.JSONDecodeError:
        return None, False


def validate_model(value):
    """Check if the value is a SQLAlchemy model instance."""
    return hasattr(value, '__table__')
