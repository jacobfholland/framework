system = [
    {
        "name": "System",
        "username": "System",
        "password": "password123"
    },
    {
        "name": "Administrator",
        "username": "Administrator",
        "password": "password123"
    }
]

permission = [
    {
        "name": "auth.permission",
        "model": "auth.permission",
        "create": True,
        "read": True,
        "update": True,
        "delete": True,
    },
    {
        "name": "auth.group",
        "model": "auth.group",
        "create": True,
        "read": True,
        "update": True,
        "delete": True,
    }
]
