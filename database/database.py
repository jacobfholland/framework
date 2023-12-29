from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.config import Config
from alembic.runtime.migration import MigrationContext

from .logger import logger


class Database:
    def __init__(self, Base, uri) -> None:
        logger.debug("Initializing database")
        self.base = Base
        self.engine = create_engine(uri)
        self.session = sessionmaker(bind=self.engine)()

        # Ensure the database is up-to-date with the latest migrations
        # self.upgrade_database()

        logger.debug("Database initialized successfully")

    def upgrade_database(self):
        alembic_cfg = Config("alembic.ini")

        # Check for changes in the schema
        if self.has_schema_changes(alembic_cfg):
            command.revision(alembic_cfg, autogenerate=True,
                             message="Auto-generated migration")

        # Upgrade the database to the latest revision
        command.upgrade(alembic_cfg, "head")

    def has_schema_changes(self, alembic_cfg):
        # Get the current database metadata
        connection = self.engine.connect()
        context = MigrationContext.configure(connection)
        current_metadata = self.base.metadata
        current_metadata.reflect(self.engine)

        # Compare current metadata with the metadata from the models
        diff = compare_metadata(context, current_metadata)

        connection.close()
        return len(diff) > 0
