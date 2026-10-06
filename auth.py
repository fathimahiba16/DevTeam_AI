import sqlite3
import hashlib
import os


DATABASE_NAME = "users.db"


def get_connection():
    """Create and return a connection to the SQLite database."""
    return sqlite3.connect(DATABASE_NAME)


def create_users_table():
    """Create the users table if it does not already exist."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def hash_password(password, salt=None):
    """Hash a password using PBKDF2."""

    if salt is None:
        salt = os.urandom(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100000
    )

    return password_hash.hex(), salt.hex()


def create_user(username, password):
    """Create a new user account."""

    username = username.strip()

    if not username or not password:
        return False, "Username and password are required."

    password_hash, salt = hash_password(password)

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (username, password_hash, salt)
            VALUES (?, ?, ?)
            """,
            (username, password_hash, salt)
        )

        connection.commit()

    except sqlite3.IntegrityError:
        connection.close()
        return False, "Username already exists."

    connection.close()

    return True, "Account created successfully."


def verify_user(username, password):
    """Check whether the username and password are correct."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT password_hash, salt
        FROM users
        WHERE username = ?
        """,
        (username.strip(),)
    )

    user = cursor.fetchone()
    connection.close()

    if user is None:
        return False

    stored_hash, stored_salt = user

    salt_bytes = bytes.fromhex(stored_salt)

    entered_hash, _ = hash_password(
        password,
        salt_bytes
    )

    return entered_hash == stored_hash