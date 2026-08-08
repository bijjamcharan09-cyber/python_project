import string
import secrets
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from database_files import password_db
from cryptography.fernet import Fernet
import pyperclip


with open("data/key.key", "rb") as file:
    key = file.read()

cipher = Fernet(key)


def encrypt_password(password):
    """Encrypt a password using Fernet."""

    return cipher.encrypt(
        password.encode()
    ).decode()


def decrypt_password(encrypted_password):
    """Decrypt a password using Fernet."""

    return cipher.decrypt(
        encrypted_password.encode()
    ).decode()

def generate_password():
    """Generate a strong random password."""

    try:
        length = int(input("Enter password length: "))

        if length < 6:
            print("Password length must be at least 6.")
            return None

    except ValueError:
        print("Please enter a valid number.")
        return None

    include_numbers = input(
        "Include numbers? (y/n): "
    ).lower()

    include_symbols = input(
        "Include symbols? (y/n): "
    ).lower()

    characters = string.ascii_letters

    if include_numbers == "y":
        characters += string.digits

    if include_symbols == "y":
        characters += string.punctuation

    password = "".join(
        secrets.choice(characters)
        for _ in range(length)
    )

    print("\n----- Generated Password -----")
    print("Password:", password)

    return password


def display_menu():

    print("\n" + "-" * 30)
    print("       PASSWORD MANAGER")
    print("-" * 30)

    print("1. Generate Password")
    print("2. Add Password")
    print("3. View Passwords")
    print("4. Update Password")
    print("5. Delete Password")
    print("6. Search Password")
    print("7. Copy Password")
    print("8. Exit")

def add_password():

    app_name = input("Enter app name: ")
    username = input("Enter username: ")
    password = input("Enter password: ")

    encrypted_password = encrypt_password(
        password
    )

    strength = input(
        "Enter password strength: "
    )

    password_db.save_password(
        app_name,
        username,
        encrypted_password,
        strength
    )

    print("Password saved successfully.")

def view_passwords():

    rows = password_db.fetch_passwords()

    if not rows:
        print("\nNo saved passwords.")
        return

    print("\n----- Saved Passwords -----")

    for row in rows:

        password_id = row[0]
        app_name = row[1]
        username = row[2]
        encrypted_password = row[3]
        strength = row[4]

        password = decrypt_password(
            encrypted_password
        )

        print(f"\nID       : {password_id}")
        print(f"App Name : {app_name}")
        print(f"Username : {username}")
        print(f"Password : {password}")
        print(f"Strength : {strength}")

def update_password():

    app_name = input(
        "Enter app name to update: "
    )

    record = password_db.find_password_by_app(
        app_name
    )

    if record is None:
        print("Password not found.")
        return

    new_password = input(
        "Enter new password: "
    )

    strength = input(
        "Enter password strength: "
    )

    encrypted_password = encrypt_password(
        new_password
    )

    password_db.update_password(
        app_name,
        encrypted_password,
        strength
    )

    print("Password updated successfully.")

def delete_password():

    app_name = input(
        "Enter app name to delete: "
    )

    record = password_db.find_password_by_app(
        app_name
    )

    if record is None:
        print("Password not found.")
        return

    password_db.delete_password(
        app_name
    )

    print("Password deleted successfully.")

def search_password():

    app_name = input(
        "Enter app name to search: "
    )

    record = password_db.find_password_by_app(
        app_name
    )

    if record is None:
        print("Password not found.")
        return

    password_id = record[0]
    app_name = record[1]
    username = record[2]
    encrypted_password = record[3]
    strength = record[4]

    password = decrypt_password(
        encrypted_password
    )

    print("\n----- Password -----")
    print("ID       :", password_id)
    print("App Name :", app_name)
    print("Username :", username)
    print("Password :", password)
    print("Strength :", strength)

def copy_password():

    app_name = input(
        "Enter app name: "
    )

    record = password_db.find_password_by_app(
        app_name
    )

    if record is None:
        print("Password not found.")
        return

    encrypted_password = record[3]

    password = decrypt_password(
        encrypted_password
    )

    try:

        pyperclip.copy(password)

        print(
            "Password copied to clipboard."
        )

    except Exception as e:

        print(
            "Clipboard error:",
            e
        )

def copy_generated_password(password):

    choice = input("Copy generated password? (y/n): ").lower()

    if choice == "y":

        try:
            pyperclip.copy(password)
            print("Password copied successfully.")

        except Exception as e:
            print("Clipboard error:", e)

    else:
        print("Copy skipped.")

def main():

    password_db.initialize_database()

    while True:

        display_menu()

        choice = input(
            "\nEnter your choice: "
        )
        if choice == "1":

            password = generate_password()
            copy_generated_password(password)

        elif choice == "2":

            add_password()

        elif choice == "3":

            view_passwords()

        elif choice == "4":

            update_password()

        elif choice == "5":

            delete_password()

        elif choice == "6":

            search_password()

        elif choice == "7":

            copy_password()

        elif choice == "8":

            print("Exiting Password Manager...")

            break

        else:

            print(
                "Invalid choice. Please try again."
            )


if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print("\nProgram interrupted.")