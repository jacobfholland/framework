import uuid


def generate_uuid() -> str:
    """Generate a unique identifier using UUID.

    Returns:
        ``str``: The generated unique identifier.
    """

    return str(uuid.uuid4())
