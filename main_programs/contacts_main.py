import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database_files import contacts_db


def add_contact():
    """Get contact details from the user and save them."""
    name = input("Enter name: ")
    phone_number = input("Enter phone number: ")
    sim_type = input("Enter SIM type: ")
    address = input("Enter address: ")
    email = input("Enter email: ")

    contacts_db.save_contact(
        name,
        phone_number,
        sim_type,
        address,
        email
    )


def view_contacts():
    """Display all contacts."""
    contacts = contacts_db.fetch_contacts()

    if not contacts:
        print("No contacts found.")
        return

    print("\nID\tName\tPhone\tSIM\tAddress\tEmail")
    print("-" * 70)

    for contact in contacts:
        print(*contact, sep="\t")


def update_contact():
    """Update an existing contact."""
    old_name = input("Enter old contact name: ")
    new_name = input("Enter new name: ")
    phone_number = input("Enter new phone number: ")
    sim_type = input("Enter new SIM type: ")
    address = input("Enter new address: ")
    email = input("Enter new email: ")

    contacts_db.update_contact_db(
        old_name,
        new_name,
        phone_number,
        sim_type,
        address,
        email
    )

    print("Contact updated successfully.")


def delete_contact():
    """Delete a contact by ID."""
    view_contacts()

    contact_id = input("\nEnter contact ID to delete: ")

    contacts_db.delete_contact_db(contact_id)

    print("Contact deleted successfully.")


def search_contact():
    """Search a contact by name."""
    name = input("Enter contact name: ")

    contacts = contacts_db.search_contact_db(name)

    if contacts:
        print("\nSearch Result")
        print("-" * 70)
        for contact in contacts:
            print(*contact, sep="\t")
    else:
        print("Contact not found.")

def display_menu():
    """Display the main menu."""
    print("=" * 17 + "\nCONTACTS MANAGEMENT\n" + "=" * 17)
    print("1. Add Contact")
    print("2. View Contacts")
    print("3. Update Contact")
    print("4. Delete Contact")
    print("5. Search Contact")
    print("6. Exit")

def main():
    contacts_db.initialize_database()

    while True:
        display_menu()

        choice = input("Enter your choice: ")

        if choice == "1":
            add_contact()

        elif choice == "2":
            view_contacts()

        elif choice == "3":
            update_contact()

        elif choice == "4":
            delete_contact()

        elif choice == "5":
            search_contact()

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()