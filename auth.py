import json
import hashlib
import os

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


# ---------- SIGNUP ----------
def signup(email, password):
    users = load_users()

    if email in users:
        return False, "User already exists"

    users[email] = hash_password(password)
    save_users(users)

    return True, "Signup successful"


# ---------- LOGIN ----------
def login(email, password):
    users = load_users()

    if email not in users:
        return False, "User not found"

    if users[email] != hash_password(password):
        return False, "Incorrect password"

    return True, "Login successful"
