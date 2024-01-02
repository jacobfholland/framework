import logging

import coloredlogs

from app.log.format import FORMAT, FORMATTER


# root_logger = logging.getLogger('root')
alembic_logger = logging.getLogger('alembic')
sqlalchemy_logger = logging.getLogger('sqlalchemy')
werkzeug_logger = logging.getLogger('werkzeug')

alembic_logger.handlers.clear()
sqlalchemy_logger.handlers.clear()
werkzeug_logger.handlers.clear()


coloredlogs.install(level="INFO", logger=alembic_logger, fmt=FORMAT)
coloredlogs.install(level="DEBUG", logger=sqlalchemy_logger, fmt=FORMAT)
coloredlogs.install(level="DEBUG", logger=werkzeug_logger, fmt=FORMAT)
