from app.config import conf
from app.log import logger


class Application:
    def __init__(self) -> None:
        self.conf = conf
        self.logger = logger

    # def init_db(self, init_db):
    #     import database
    #     database.db = init_db.session

    def init_db(self, init_db):
        if self.conf.DATABASE:
            import database
            database.session = init_db.session

    def init_auth(self):
        if self.conf.DATABASE and self.conf.AUTH:
            from auth.user import User
            User().seed()
