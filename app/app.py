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
        from auth.permission import Permission
        Permission().seed()

        from auth.group import Group
        Group().seed()

        from auth.user import User
        User().seed()

        logger.critical("+++++++++++++++++++++++++++++++++++++++++++++++++++")
        Group(name="testing", permissions=Permission().get().all()).create()
