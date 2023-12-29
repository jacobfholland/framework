from app import app

if app.conf.DATABASE:
    from database import db
    if app.conf.AUTH:
        from modules.auth.user import User

# User(name="jacob", username="ndysu", password="test123").create()
users = User().get(strict=False).all()
for user in users:
    # user.update(name="updated_name", password="omg")
    user.delete()

User().seed()
# users.archive()

# user.update(name="updated_name", password="omg")
# user.update({"name": "updated_name", "password": "poopies"})
# print(vars(users))
