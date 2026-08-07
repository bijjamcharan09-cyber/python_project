import ast
import sqlite3

DB_NAME = "data/contact_book.db"

def connect_database():
    """
    Connects to the SQLite database.
    If the database does not exist, it will be created automatically.
    """
    connection = sqlite3.connect(DB_NAME)
    return connection


def create_table():
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts(
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
    """
    Initializes the database by creating the required table.
    """
    create_table()
    print("Database initialized successfully.")

def display_menu(): #This function displays the main menu of the contact book application.
    print("\n===== Contact Book Menu =====")
    print("1. Add Contact")
    print("2. View Contacts")
    print("3. Update Contact")
    print("4. Delete Contact")
    print("5. Search Contact")
    print("6. Exit")

def fetch_contacts():
    """
    Retrieves all contacts records from the database.
    """
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM contacts
    """)

    contacts = cursor.fetchall()

    connection.close()
    if not contacts:
        print("\n----------\nNo Contacts\n----------")
    else:
        return contacts

def save_contact(name, phone_number, sim_type, address, email):
    connection = connect_database()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO contacts(
                name,
                phone_number,
                sim_type,
                address,
                email
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            name,
            phone_number,
            sim_type,
            address,
            email
        ))

        connection.commit()
        print("Contact saved successfully.")

    except sqlite3.Error as e:
        print("Database Error:", e)

    finally:
        connection.close()

def search_contact_db(name):
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

def delete_contact_db(id):
    fetch_contacts()  # Display contacts before deletion to check id. 
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM contacts
        WHERE id = ?
    """, (id,))

    connection.commit()
    connection.close()


def main(): # This is the main function that runs the contact book application.
    contacts = fetch_contacts()

    while True:
        display_menu()

        choice = input("Enter your choice: ")

        if choice == "1":
            save_contact(
                input("Enter name: "),
                input("Enter phone number: "),
                input("Enter SIM type: "),
                input("Enter address: "),
                input("Enter email: ")
            )

        elif choice == "2":
            fetch_contacts()

        elif choice == "3":
             update_contact_db(
                            input("Enter old contact name: "),
                            input("Enter new name: "),
                            input("Enter new phone number: "),
                            input("Enter new SIM type: "),
                            input("Enter new address: "),
                            input("Enter new email: ")
                        )

        elif choice == "4":
             delete_contact_db(input("Enter contact ID to delete: "))

        elif choice == "5":
            search_contact_db(input("Enter contact name to search: "))

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()