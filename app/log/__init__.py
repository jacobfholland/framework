from app.config import conf
from .external import configure_external_loggers
from .logger import create_logger


logger = create_logger(f"{conf.APP_NAME.lower()}.app")
