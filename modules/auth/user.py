from bcrypt import checkpw, gensalt, hashpw
from sqlalchemy import Column, Integer, String

from app import app
from app.utils.generate import generate_uuid

from .logger import logger

session_store = {}

try:
    if app.conf.DATABASE and app.conf.AUTH:
        from database.model import Model

        class User(Model):
            name = Column(String)
            username = Column(String)
            password = Column(String)

            def __repr__(self):
                return f"<User(name={self.name})>"

            def hash_password(password):
                return hashpw(password.encode('utf-8'), gensalt())

            def check_password_hash(password, hash):
                return checkpw(password.encode('utf-8'), hash)

            def create_session(user_id):
                session_id = generate_uuid()
                session_store[session_id] = {'user_id': user_id}
                return session_id

            def get_current_session_id():
                # Implement your method to retrieve the current session ID, usually from the request cookie
                pass

            def invalidate_session(session_id):
                if session_id in session_store:
                    del session_store[session_id]

            def login(self, username, password):
                user = self.query.filter_by(username=username).first()
                if user and self.check_password_hash(user.password, password):
                    # Create session and return success
                    session_id = self.create_session(user.id)
                    return True, session_id  # or a more secure token
                return False, None

            def logout(self):
                session_id = self.get_current_session_id()  # Implement this
                if session_id:
                    self.invalidate_session(session_id)
                    return True
                return False

        logger.debug(f"User model imported")
except Exception as e:
    logger.warning(f"Unable to import model User")
