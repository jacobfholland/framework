from datetime import datetime

from sqlalchemy import and_, or_
from sqlalchemy.inspection import inspect
from app.utils.bind import bind_values, update_kwargs

import database
from app.log.logger import create_logger
from app.utils.log import disable_logging
from database.filter import Filter
from database.query import Query
from database.utils import select_func

logger = create_logger(__name__)


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

    def query(self, strict=True, **filters):
        # print("++++++++++++", filters)
        filter_conditions = self.filter(
            strict=strict, **filters)

        query = database.session.query(
            self.__class__).filter(filter_conditions)
        print("++++++++++++", query)
        logger.debug(
            f"Constructed query for {self.__class__.__name__}: {query}")
        return query

    def update_filters(self, *args, **filters):
        if "deleted_at" not in filters:
            filters["deleted_at"] = None
        if len(args) == 1 and isinstance(args[0], dict):
            filters.update(args[0])

        # for k, v in filters.items():
        #     if hasattr(v, "__table__"):
        #         filters[k] = v.id

        return filters

    def strip_relationships(self, filters):
        # TODO: Make this only remove model objects, not entire field
        # This will allow searching for relationship type fields
        relationships = self.get_relationship_names()
        strip_relationships = {}
        for k, v in filters.items():
            if not k in relationships:
                strip_relationships[k] = v
        return strip_relationships

    def get(self, *args, func=and_, **filters):
        try:

            # filters.update(self.__dict__) # Add values from current model
            filters = update_kwargs(*args, **filters)
            filter = Filter(self.__class__, **filters)
            func = select_func(func)
            query = Query(filter, func)
            logger.debug(
                f"Retrieving {self.__class__.__name__} with filter: {filter}")
            self.log_results(query)
            return query.results
        except Exception as e:
            logger.error(
                f"{type(e)} Failed to retrieve {self.__class__.__name__} due to: {e}")

    def log_results(self, query):
        results = query.results.all()
        result_count = len(results)

        if result_count > 1:
            ids = [str(result.id) for result in results]
            logger.info(
                f"Multiple ({result_count}) {self.__class__.__name__} instances retrieved with IDs: {ids}")
        elif result_count == 1:
            logger.debug(
                f"Successfully retrieved record {self.__class__.__name__}: {vars(results[0])}")
            logger.info(
                f"Successfully retrieved {self.__class__.__name__} with ID: {results[0].id}")
        else:
            logger.warning(
                f"No {self.__class__.__name__} instances found with the provided filters.")

    def create(self, *args, **values):
        try:
            logger.debug(
                f"Creating {self.__class__.__name__} with attributes: {vars(self)}")
            values = update_kwargs(*args, **values)
            bind_values(self, values)
            database.session.add(self)
            database.session.commit()
            logger.info(
                f"Successfully created {self.__class__.__name__} with ID: {self.id}")
            return self
        except Exception as e:
            logger.error(
                f"{type(e)} Creation failed for {self.__class__.__name__}: {e}")
            database.session.rollback()

    def create_not_exists(self, filters, *args, **values):
        try:
            logger.debug(
                f"Attempting to create {self.__class__.__name__} if not exists with filters: {filters}, attributes: {values}")
            values = update_kwargs(*args, **values)
            existing = self.get(**filters).all()
            if not existing:
                self.__class__().create(**values)
        except Exception as e:
            logger.error(
                f"{type(e)} Creation failed for {self.__class__.__name__}: {e}")
            database.session.rollback()

    def update(self, *args, **values):
        try:
            values = update_kwargs(*args, **values)
            bind_values(self, values)
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
            return self
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
            return self
        except Exception as e:
            logger.error(
                f"{type(e)} Archiving failed for {self.__class__.__name__}: {e}")
            database.session.rollback()
