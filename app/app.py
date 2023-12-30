from app.config import conf
from app.log import logger


class Application:
    def __init__(self) -> None:
        import modules
        self.conf = conf
        self.logger = logger

    def init_db(self, init_db, name="session"):
        import database
        setattr(database, name, init_db.session)

    def init_auth(self):
        import auth
        from auth.user import User
        User().seed()
