from sqlalchemy import and_, or_
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
        from auth.group import Group
        from auth.user import User
        from database.seed import Seed
        logger.critical(
            "++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        Permission().seed()
        Group().seed()
        User().seed()
        # name = "User"
        # permissions = Permission().get().all()
        # seed = {"name": name, "permissions": permissions}

        # existing = Group().get(name="User").all()
        # if not existing:
        #     records_ids = []
        #     for record in permissions:
        #         records_ids.append(record.id)
        #     group = Group().create(**seed)
