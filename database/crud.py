from sqlalchemy import and_, or_

from app import app

from .logger import logger


class Crud:

    def filter(self, strict=False, **filters):
        conditions = [
            getattr(self.__class__, field) == value
            for field, value in filters.items()
            if hasattr(self.__class__, field)
        ]
        log_condition = and_ if strict else or_
        conditions_str = [str(condition) for condition in conditions]
        logger.debug(
            f"Building filter for {self.__class__.__name__} with {log_condition.__name__} conditions: {conditions_str}")
        return log_condition(*conditions)

    def query(self, strict=False, **filters):
        filter_conditions = self.filter(strict, **filters)
        query = app.db.session.query(self.__class__).filter(filter_conditions)
        logger.debug(
            f"Constructed query for {self.__class__.__name__}: {query}")
        return query

    def get(self, *args, strict=False, **filters):
        try:
            # Check if a single dictionary argument is provided
            if len(args) == 1 and isinstance(args[0], dict):
                filters.update(args[0])

            logger.debug(
                f"Attempting to retrieve {self.__class__.__name__} with filters: {filters}")
            return self.query(strict=strict, **filters)
        except Exception as e:
            logger.error(
                f"Retrieval failed for {self.__class__.__name__}: {e}")

    def create(self):
        try:
            logger.debug(
                f"Attempting to create {self.__class__.__name__} with attributes: {vars(self)}")
            app.db.session.add(self)
            app.db.session.commit()
            logger.info(
                f"Successfully created {self.__class__.__name__} with ID: {self.id}")
        except Exception as e:
            logger.error(f"Creation failed for {self.__class__.__name__}: {e}")
            app.db.session.rollback()

    def update(self, *args, **values):
        try:
            if len(args) == 1 and isinstance(args[0], dict):
                values.update(args[0])
            logger.debug(
                f"Attempting to update {self.__class__.__name__} with values: {values}")
            for key, value in values.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            app.db.session.commit()
            logger.info(
                f"Successfully updated {self.__class__.__name__} with ID: {self.id}")
            return self
        except Exception as e:
            logger.error(f"Update failed for {self.__class__.__name__}: {e}")
            app.db.session.rollback()

    def delete(self):
        try:
            logger.debug(
                f"Attempting to delete {self.__class__.__name__} with ID: {self.id}")
            app.db.session.delete(self)
            app.db.session.commit()
            logger.info(
                f"Successfully deleted {self.__class__.__name__} with ID: {self.id}")
        except Exception as e:
            logger.error(f"Deletion failed for {self.__class__.__name__}: {e}")
            app.db.session.rollback()
