from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from alembic import command
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.autogenerate.api import compare_metadata

from app.log.logger import create_logger


logger = create_logger("database.database")


class Database:
    def __init__(self, Base, uri) -> None:
        self.base = Base
        self.engine = create_engine(uri)
        self.base.metadata.create_all(bind=self.engine)
        self.session = sessionmaker(bind=self.engine)()

        # Ensure the database is up-to-date with the latest migrations
        self.sync_schema()

        logger.debug("Database initialized successfully")

    def sync_schema(self):
        logger.debug("Beginning database schema sync")
        alembic_cfg = Config("alembic.ini")
        connection = self.engine.connect()
        context = MigrationContext.configure(connection)

        logger.debug("Comparing database schema against context")
        diff = compare_metadata(context, self.base.metadata)

        if diff:
            logger.warning("Database schema changes detected")
            logger.info("Upgrading database")
            # If there are differences, autogenerate a migration script
            command.revision(alembic_cfg, autogenerate=True,
                             message="Auto-generated migration for schema sync")
            # Apply the migration to the database
            command.upgrade(alembic_cfg, "head")
        else:
            logger.info("No database schema changes detected.")
        logger.debug("Database schema sync complete")
        connection.close()

    def has_schema_changes(self, alembic_cfg):
        # This function may be redundant now as we're handling it in sync_schema
        connection = self.engine.connect()
        context = MigrationContext.configure(connection)

        diff = compare_metadata(context, self.base.metadata)

        connection.close()
        return len(diff) > 0
