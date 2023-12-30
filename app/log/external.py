import logging
import coloredlogs
from app.log.format import FORMAT, FORMATTER


def configure_external_loggers():
    # Retrieve the loggers for Alembic and SQLAlchemy
    alembic_logger = logging.getLogger('alembic')
    sqlalchemy_logger = logging.getLogger('sqlalchemy')

    # Set the logging level for these loggers
    alembic_logger.setLevel(logging.INFO)
    sqlalchemy_logger.setLevel(logging.WARNING)

    # Apply the same handlers and formatter you use for your main logger
    for handler in logging.getLogger().handlers:
        alembic_logger.addHandler(handler)
        sqlalchemy_logger.addHandler(handler)

    # Optionally, if you want to apply colored logs to these loggers
    coloredlogs.install(level="INFO", logger=alembic_logger, fmt=FORMAT)
    coloredlogs.install(level="WARNING", logger=sqlalchemy_logger, fmt=FORMAT)
