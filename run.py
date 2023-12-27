from app import app
from app.log.logger import create_logger


logger = create_logger("example")
logger.debug("Example message")
