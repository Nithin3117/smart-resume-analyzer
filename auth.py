import json
import os
import hashlib
import re

USER_FILE = "users.json"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)


def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)


def signup(email, password):
    users = load_users()

    if not is_valid_email(email):
        return False, "Invalid email"

    if email in users:
        return False, "User exists"

    users[email] = {"password": hash_password(password)}
    save_users(users)

    return True, "Signup successful"


def login(email, password):
    users = load_users()

    if email in users and users[email]["password"] == hash_password(password):
        return True

    return False


def reset_password(email, new_password):
    users = load_users()

    if email not in users:
        return False, "User not found"

    users[email]["password"] = hash_password(new_password)
    save_users(users)

    return True, "Password updated"
