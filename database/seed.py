from app.log.logger import create_logger
from app.utils.log import disable_logging

logger = create_logger(__name__)


class Seed:
    def seeds(self):
        return []

    @disable_logging
    def seed(self):
        if self._seed_key:
            for record in self.seeds():
                filters = {self._seed_key: record.get(self._seed_key)}
                self.__class__().create_not_exists(filters, **record)
