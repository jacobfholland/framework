from app.config import conf
from app.log import logger


class Application:
    def __init__(self) -> None:
        self.conf = conf
        self.logger = logger
