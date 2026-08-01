import ast

FILENAME = "data/contacts.txt"

def display_menu(): #This function displays the main menu of the contact book application.
    print("\n===== Contact Book Menu =====")
    print("1. Add Contact")
    print("2. View Contacts")
    print("3. Search Contact")
    print("4. Update Contact")
    print("5. Delete Contact")
    print("6. Exit")

def load_contacts(): #This function loads all the previous contacts from a file.
    contacts = []

    try:
        with open(FILENAME, "r") as file:
            for line in file:
                contacts.append(ast.literal_eval(line.strip()))
    except FileNotFoundError:
        pass

    return contacts


def save_contacts(contacts): #This function saves the contacts into a file and uses exception handling.
    try:
        with open(FILENAME, "w") as file:
            for contact in contacts:
                file.write(str(contact) + "\n")
    except Exception as e:
        print(f"Error saving contacts: {e}")


def add_contact(contacts): # This function prompts the user to enter a new contact and saves it to the file.
    name = input("Enter name: ").capitalize()
    phone = input("Enter phone number: ")

    contact = {
        "name": name,
        "phone": phone
    }

    contacts.append(contact)
    save_contacts(contacts)

    print("-"*27)
    print("Contact added successfully.")
    print("-"*27)


def view_contacts(contacts): # This function displays all contacts.
    if not contacts:
        print("No contacts found.")
        return

    for i, contact in enumerate(contacts):
        print("-"*30)
        print(f"{i + 1}. Name = {contact['name']}")
        print(f"   Phone number = {contact['phone']}")
        print("-"*30)
        print()


def search_contact(contacts): # This function searches for a contact by name and displays the contact information if found.
    name = input("Enter name to search: ").capitalize()

    found = False

    for contact in contacts:
        if contact["name"].capitalize() == name:
            print("-"*24)
            print(f"Name: {contact['name']}")
            print(f"Phone number: {contact['phone']}")
            print("-"*24)
            found = True

    if not found:
        print("-"*24)
        print("Contact not found.")
        print("-"*24)


def update_contact(contacts): # This function updates the phone number of an existing contact.
    name = input("Enter contact name to update: ").capitalize()

    for contact in contacts:
        if contact["name"].capitalize() == name:
            contact["name"] = input("Enter new name: ").capitalize()
            contact["phone"] = input("Enter new phone number: ")
            save_contacts(contacts)
            print("-"*24)
            print("Contact updated successfully.")
            print("-"*24)
            return

    print("Contact not found.")


def delete_contact(contacts): # This function deletes a contact by name and saves the updated contact list to the file.
    name = input("Enter contact name to delete: ").capitalize() 

    for contact in contacts:
        if contact["name"].capitalize() == name:
            contacts.remove(contact)
            save_contacts(contacts)
            print("-"*29)
            print("Contact deleted successfully.")
            print("-"*29)
            return

    print("Contact not found.")


def main(): # This is the main function that runs the contact book application.
    contacts = load_contacts()

    while True:
        display_menu()

        choice = input("Enter your choice: ")

        if choice == "1":
            add_contact(contacts)

        elif choice == "2":
            view_contacts(contacts)

        elif choice == "3":
            search_contact(contacts)

        elif choice == "4":
            update_contact(contacts)

        elif choice == "5":
            delete_contact(contacts)

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()