import sqlite3

DB_NAME = "data/contact_book.db"


def connect_database():
    """Connect to the SQLite database."""
    return sqlite3.connect(DB_NAME)


def create_table():
    """Create contacts table if it doesn't exist."""
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            sim_type TEXT NOT NULL,
            address TEXT,
            email TEXT
        )
    """)

    connection.commit()
    connection.close()


def initialize_database():
    """Initialize the database."""
    create_table()
    print("Database initialized successfully.")


def fetch_contacts():
    """Retrieve all contacts."""
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM contacts")
    contacts = cursor.fetchall()

    connection.close()
    return contacts


def save_contact(name, phone_number, sim_type, address, email):
    """Insert a new contact."""
    connection = connect_database()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO contacts
            (name, phone_number, sim_type, address, email)
            VALUES (?, ?, ?, ?, ?)
        """, (name, phone_number, sim_type, address, email))

        connection.commit()
        print("Contact saved successfully.")

    except sqlite3.Error as e:
        print("Database Error:", e)

    finally:
        connection.close()


def search_contact_db(name):
    """Search contact by name."""
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM contacts
        WHERE name = ?
    """, (name,))

    contact = cursor.fetchall()
    connection.close()

    return contact


def update_contact_db(old_name, new_name, phone_number,
                      sim_type, address, email):
    """Update an existing contact."""
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE contacts
        SET
            name = ?,
            phone_number = ?,
            sim_type = ?,
            address = ?,
            email = ?
        WHERE name = ?
    """, (
        new_name,
        phone_number,
        sim_type,
        address,
        email,
        old_name
    ))

    connection.commit()
    connection.close()


def delete_contact_db(contact_id):
    """Delete contact by ID."""
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM contacts
        WHERE id = ?
    """, (contact_id,))

    connection.commit()
    connection.close()