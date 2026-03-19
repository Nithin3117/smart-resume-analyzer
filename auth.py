import json
import os
import hashlib

USER_FILE = "users.json"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)


def signup(username, password):
    users = load_users()

    if username in users:
        return False, "User already exists"

    users[username] = {
        "password": hash_password(password),
        "history": []
    }

    save_users(users)
    return True, "Signup successful"


def login(username, password):
    users = load_users()

    if username in users:
        if users[username]["password"] == hash_password(password):
            return True
    return False


def get_user(username):
    users = load_users()
    return users.get(username, {})
