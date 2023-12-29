from datetime import datetime
from sqlalchemy import and_, or_

from app import app
from app.log.logger import create_logger

logger = create_logger("database.crud")


class Crud:

    def filter(self, strict=True, quiet_log=False, **filters):
        conditions = [
            getattr(self.__class__, field) == value
            for field, value in filters.items()
            if hasattr(self.__class__, field)
        ]
        log_condition = and_ if strict else or_
        conditions_str = [str(condition) for condition in conditions]
        if not quiet_log:
            logger.debug(
                f"Building filter for {self.__class__.__name__} with {log_condition.__name__} conditions: {conditions_str}")
        return log_condition(*conditions)

    def query(self, strict=True, quiet_log=False, **filters):
        filter_conditions = self.filter(
            strict=strict, quiet_log=quiet_log, **filters)
        query = app.db.session.query(self.__class__).filter(filter_conditions)
        if not quiet_log:
            logger.debug(
                f"Constructed query for {self.__class__.__name__}: {query}")
        return query

    def update_filters(self, *args, **filters):
        if "deleted_at" not in filters:
            filters["deleted_at"] = None
        if len(args) == 1 and isinstance(args[0], dict):
            filters.update(args[0])
        return filters

    def get(self, *args, strict=True, quiet_log=False, **filters):
        try:
            filters = self.update_filters(*args, **filters)
            if not quiet_log:
                logger.debug(
                    f"Retrieving {self.__class__.__name__} with filters: {filters}")
            query = self.query(strict=strict, quiet_log=quiet_log, **filters)

            results = query.all()
            result_count = len(results)

            if result_count > 1:
                ids = [str(result.id) for result in results]
                if not quiet_log:
                    logger.info(
                        f"Multiple ({result_count}) {self.__class__.__name__} instances retrieved with IDs: {ids}")
            elif result_count == 1:
                if not quiet_log:
                    logger.debug(
                        f"Retrieved record {self.__class__.__name__} with ID: {vars(results[0])}")
                    logger.info(
                        f"Successfully retrieved {self.__class__.__name__} with ID: {results[0].id}")
            else:
                if not quiet_log:
                    logger.warning(
                        f"No {self.__class__.__name__} instances found with the provided filters.")
            return query
        except Exception as e:
            logger.error(
                f"{type(e)} Failed to retrieve {self.__class__.__name__} due to: {e}")

    def create(self, quiet_log=False):
        try:
            if not quiet_log:
                logger.debug(
                    f"Attempting to create {self.__class__.__name__} with attributes: {vars(self)}")
            app.db.session.add(self)
            app.db.session.commit()
            if not quiet_log:
                logger.info(
                    f"Successfully created {self.__class__.__name__} with ID: {self.id}")
        except Exception as e:
            logger.error(
                f"{type(e)} Creation failed for {self.__class__.__name__}: {e}")
            app.db.session.rollback()

    def create_not_exists(self, quiet_log=False, **values):
        try:
            if not quiet_log:
                logger.debug(
                    f"Attempting to create {self.__class__.__name__} with attributes: {values}")
            existing = self.get(quiet_log=True, **values).all()
            if not existing:
                record = self.__class__(**values)
                app.db.session.add(record)
                app.db.session.commit()
                if not quiet_log:
                    logger.info(
                        f"Successfully created {self.__class__.__name__} with ID: {self.id}")
            else:
                if not quiet_log:
                    logger.info(
                        f"Record already exists {self.__class__.__name__} with ID: {existing[0].id}")
        except Exception as e:
            logger.error(
                f"{type(e)} Creation failed for {self.__class__.__name__}: {e}")
            app.db.session.rollback()

    def update(self, *args, quiet_log=False, **values):
        try:
            if len(args) == 1 and isinstance(args[0], dict):
                values.update(args[0])
            if not quiet_log:
                logger.debug(
                    f"Attempting to update {self.__class__.__name__} with values: {values}")
            for key, value in values.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            app.db.session.commit()
            if not quiet_log:
                logger.info(
                    f"Successfully updated {self.__class__.__name__} with ID: {self.id}")
            return self
        except Exception as e:
            logger.error(
                f"{type(e)} Update failed for {self.__class__.__name__}: {e}")
            app.db.session.rollback()

    def delete(self, quiet_log=False, soft=False):
        try:
            if not quiet_log:
                logger.debug(
                    f"Attempting to delete {self.__class__.__name__} with ID: {self.id}")
            self.deleted_at = datetime.utcnow()
            if not soft:
                app.db.session.delete(self)
            app.db.session.commit()
            if not quiet_log:
                logger.info(
                    f"Successfully deleted {self.__class__.__name__} with ID: {self.id}")
        except Exception as e:
            logger.error(
                f"{type(e)} Deletion failed for {self.__class__.__name__}: {e}")
            app.db.session.rollback()

    def archive(self, quiet_log=False):
        try:
            if not quiet_log:
                logger.debug(
                    f"Attempting to archive {self.__class__.__name__} with ID: {self.id}")
            self.deleted_at = datetime.utcnow()
            app.db.session.commit()
            if not quiet_log:
                logger.info(
                    f"Successfully archived {self.__class__.__name__} with ID: {self.id}")
        except Exception as e:
            logger.error(
                f"{type(e)} Archiving failed for {self.__class__.__name__}: {e}")
            app.db.session.rollback()
