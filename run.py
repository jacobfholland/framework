from app import app

if app.conf.DATABASE:
    from database import db
    if app.conf.AUTH:
        from modules.auth.user import User

user = User().get(name="updated_name").first()
user.update(name="updated_name", password="omg")
user.update({"name": "updated_name", "password": "poopies"})
print(vars(user))
