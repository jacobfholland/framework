from app.log.logger import create_logger
from app.utils.log import disable_logging


logger = create_logger("database.seed")


class Seed:

    # @disable_logging
    def seed(self):
        logger.debug(
            f"Seeding {self.__class__.__name__} model table '{self.__class__.__tablename__}'")
        for seed in self.seeds():
            self.create_not_exists(**seed)

    def seeds(self):
        return []
