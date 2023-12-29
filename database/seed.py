from app.log.logger import create_logger


logger = create_logger("database.seed")


class Seed:
    def seed(self, quiet_log=True):
        if not quiet_log:
            logger.debug(
                f"Seeding {self.__class__.__name__} model table '{self.__class__.__tablename__}'")
        for seed in self.seeds():
            self.create_not_exists(quiet_log=quiet_log, **seed)

    def seeds(self):
        return []
