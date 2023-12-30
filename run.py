# main.py
from app.app import Application
from database.database import Database

# Create an Application instance
app = Application()

# Create a Database instance and initialize the global db_instance variable
db = Database("sqlite:///example.db")
app.init_db(db)

try:
    import database
    from auth.user import User
    User(name="databaseguy", password="pooop").create()
except Exception as e:
    pass
