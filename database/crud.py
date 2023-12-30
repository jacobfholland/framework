from datetime import datetime
from sqlalchemy import and_, or_

from app.log.logger import create_logger
from app.utils.log import disable_logging

import database

logger = create_logger("database.crud")


class Crud:

    def filter(self, strict=True, **filters):
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

    def update_filters(self, *args, **filters):
        if "deleted_at" not in filters:
            filters["deleted_at"] = None
        if len(args) == 1 and isinstance(args[0], dict):
            filters.update(args[0])
        return filters

    def query(self, strict=True, **filters):
        filter_conditions = self.filter(
            strict=strict, **filters)
        query = database.session.query(
            self.__class__).filter(filter_conditions)
        logger.debug(
            f"Constructed query for {self.__class__.__name__}: {query}")
        return query

    def get(self, *args, strict=True, **filters):
        try:
            filters = self.update_filters(*args, **filters)
            logger.debug(
                f"Retrieving {self.__class__.__name__} with filters: {filters}")
            query = self.query(strict=strict, **filters)

            results = query.all()
            result_count = len(results)

            if result_count > 1:
                ids = [str(result.id) for result in results]
                logger.info(
                    f"Multiple ({result_count}) {self.__class__.__name__} instances retrieved with IDs: {ids}")
            elif result_count == 1:
                logger.debug(
                    f"Retrieved record {self.__class__.__name__} with ID: {vars(results[0])}")
                logger.info(
                    f"Successfully retrieved {self.__class__.__name__} with ID: {results[0].id}")
            else:
                logger.warning(
                    f"No {self.__class__.__name__} instances found with the provided filters.")
            return query
        except Exception as e:
            logger.error(
                f"{type(e)} Failed to retrieve {self.__class__.__name__} due to: {e}")

    def create(self, **values):
        try:
            logger.debug(
                f"Attempting to create {self.__class__.__name__} with attributes: {vars(self)}")
            self.update_values(values)
            database.session.add(self)
            database.session.commit()
            logger.info(
                f"Successfully created {self.__class__.__name__} with ID: {self.id}")
        except Exception as e:
            logger.error(
                f"{type(e)} Creation failed for {self.__class__.__name__}: {e}")
            database.session.rollback()

    def create_not_exists(self, **values):
        try:
            logger.debug(
                f"Attempting to create {self.__class__.__name__} with attributes: {values}")
            existing = self.get(**values).all()
            if not existing:
                record = self.__class__(**values)
                database.session.add(record)
                database.session.commit()
                logger.info(
                    f"Successfully created {self.__class__.__name__} with ID: {self.id}")
            else:
                logger.info(
                    f"Record already exists {self.__class__.__name__} with ID: {existing[0].id}")
        except Exception as e:
            logger.error(
                f"{type(e)} Creation failed for {self.__class__.__name__}: {e}")
            database.session.rollback()

    def update(self, *args, **values):
        try:
            if len(args) == 1 and isinstance(args[0], dict):
                values.update(args[0])
                logger.debug(
                    f"Attempting to update {self.__class__.__name__} with values: {values}")
            for key, value in values.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            database.session.commit()
            logger.info(
                f"Successfully updated {self.__class__.__name__} with ID: {self.id}")
            return self
        except Exception as e:
            logger.error(
                f"{type(e)} Update failed for {self.__class__.__name__}: {e}")
            database.session.rollback()

    def delete(self, soft=False):
        try:
            logger.debug(
                f"Attempting to delete {self.__class__.__name__} with ID: {self.id}")
            self.deleted_at = datetime.utcnow()
            if not soft:
                database.session.delete(self)
            database.session.commit()
            logger.info(
                f"Successfully deleted {self.__class__.__name__} with ID: {self.id}")
        except Exception as e:
            logger.error(
                f"{type(e)} Deletion failed for {self.__class__.__name__}: {e}")
            database.session.rollback()

    def archive(self):
        try:
            logger.debug(
                f"Attempting to archive {self.__class__.__name__} with ID: {self.id}")
            self.deleted_at = datetime.utcnow()
            database.session.commit()
            logger.info(
                f"Successfully archived {self.__class__.__name__} with ID: {self.id}")
        except Exception as e:
            logger.error(
                f"{type(e)} Archiving failed for {self.__class__.__name__}: {e}")
            database.session.rollback()
