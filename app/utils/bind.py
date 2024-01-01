from app.log.logger import create_logger


logger = create_logger(__name__)


def bind_values(obj, values):
    data = {**obj.__dict__, **values}
    for key, value in data.items():
        if hasattr(obj, key):
            setattr(obj, key, value)
        else:
            logger.warning(
                f"Key {key} does not exist on {obj.__class__.__name__}")


def update_kwargs(*args, **kwargs):
    if len(args) == 1 and isinstance(args[0], dict):
        kwargs.update(args[0])
        return kwargs
    return kwargs
