from sqlalchemy import or_
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
        import database
        from database.filter import Filter
        logger.critical("+++++++++++++++++++++++++++++++++++++++++++++++++++")
        from auth.group import Group
        from auth.permission import Permission

        data = {"name": "System", "permissions.id": [1, 2]}
        filter = Filter(Group, **data)

        records = database.session.query(
            Group).filter(or_(*filter.filter)).all()
        print(vars(filter))
