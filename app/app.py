from app.config import conf
from app.log import logger


class Application:
    def __init__(self) -> None:

        self.conf = conf
        self.logger = logger

    def init_db(self, init_db, name="session"):
        import database
        setattr(database, name, init_db.session)
        setattr(database, "db", init_db)

    def init_auth(self):
        import auth
        from database.filter import Filter
        logger.critical("+++++++++++++++++++++++++++++++++++++++++++++++++++")
        data = {"name": "System", "permissions.id": 1}
        from auth.group import Group
        filter = Filter(Group, **data)
