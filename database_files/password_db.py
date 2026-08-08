import sqlite3


DB_NAME = "data/passwords_manager(2).db"


def connect_database():
    """Connect to the SQLite database."""
    return sqlite3.connect(DB_NAME)


def create_table():
    """Create the passwords table if it does not exist."""

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            app_name TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            strength TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def initialize_database():
    """Initialize the password database."""
    create_table()
    print("Database initialized successfully.")


def save_password(app_name, username, password, strength):
    """Save an encrypted password record."""

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO passwords(
            app_name,
            username,
            password,
            strength
        )
        VALUES (?, ?, ?, ?)
    """, (
        app_name,
        username,
        password,
        strength
    ))

    connection.commit()
    connection.close()


def fetch_passwords():
    """Retrieve all saved password records."""

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM passwords
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


def find_password_by_app(app_name):
    """Find a password record by application name."""

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM passwords
        WHERE LOWER(app_name) = ?
    """, (app_name.lower(),))

    row = cursor.fetchone()

    connection.close()

    return row


def update_password(app_name, encrypted_password, strength):
    """Update an existing password."""

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE passwords
        SET password = ?,
            strength = ?
        WHERE LOWER(app_name) = ?
    """, (
        encrypted_password,
        strength,
        app_name.lower()
    ))

    connection.commit()

    rows_updated = cursor.rowcount

    connection.close()

    return rows_updated


def delete_password(app_name):
    """Delete a saved password."""

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM passwords
        WHERE LOWER(app_name) = ?
    """, (app_name.lower(),))

    connection.commit()

    rows_deleted = cursor.rowcount

    connection.close()

    return rows_deleted


def fetch_password_list():
    """Retrieve ID, app name and username."""

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, app_name, username
        FROM passwords
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


def fetch_password_by_id(password_id):
    """Retrieve an encrypted password using its ID."""

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT password
        FROM passwords
        WHERE id = ?
    """, (password_id,))

    result = cursor.fetchone()

    connection.close()

    return result