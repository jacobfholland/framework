# main.py
from app.app import Application
from database.database import Database

# Create an Application instance
app = Application()
db = Database("sqlite:///example.db")
app.init_db(db)
app.init_auth()
