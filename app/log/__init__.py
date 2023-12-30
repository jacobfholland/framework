from app.config import conf

from .logger import create_logger

logger = create_logger(f"{conf.APP_NAME.lower()}.app")
