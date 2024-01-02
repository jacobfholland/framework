from sqlalchemy import and_, or_
from app.config import conf
from app.log import logger
from app.config.environment import Environment


class Application:
    def __init__(self) -> None:
        self.env = Environment()
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
        Permission().seed()
        Group().seed()
        User().seed()

    def init_server(self):
        import server
        from server.server import Server
        from server.decorator import route
        from auth.user import User

        # TODO: Make this built into a routes() function inside the class that runs on import somehow
        @route(User, "/", methods=["GET"], url_prefix="/")
        def get(cls, request):
            records = cls().get(request.json).all()
            return records
        Server().run()
