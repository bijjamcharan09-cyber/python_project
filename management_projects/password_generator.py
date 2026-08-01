import random as rd
import string as st
import pyperclip
import os 
import sqlite3
from cryptography.fernet import Fernet
connection = sqlite3.connect("data/passwords_manager.db")
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    app_name TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    strength TEXT NOT NULL
    )
    """
)
connection.commit()

LOCK_FILE = "data/lock.txt"

def setup_lock():
    if not os.path.exists(LOCK_FILE):

        print("----- First Time Setup -----")

        while True:
            password = input("Create a lock password: ")
            confirm = input("Confirm password: ")

            if password == confirm:
                with open(LOCK_FILE, "w") as file:
                    file.write(password)

                print("Lock password created successfully.")
                break

            else:
                print("Passwords do not match. Try again.")

def set_lock_password():

    if not get_lock_password():
        print("Wrong current password!")
        return

    while True:
        new_password = input("Enter new lock password: ")
        confirm_password = input("Confirm new lock password: ")

        if new_password != confirm_password:
            print("Passwords do not match. Try again.\n")
            continue

        if len(new_password) < 6:
            print("Password must be at least 6 characters long.\n")
            continue

        with open(LOCK_FILE, "w") as file:
            file.write(new_password)

        print("Lock password updated successfully.")
        break

def get_lock_password():

    with open(LOCK_FILE, "r") as file:
        saved_password = file.read().strip()

    entered_password = input("Enter lock password: ")

    if entered_password == saved_password:
        return True

    print("Incorrect password!")

    choice = input("Forgot password? (y/n): ").lower()

    if choice == "y":
        reset_lock_password()

    return False

def reset_lock_password():

    print("----- Reset Lock Password -----")

    answer = input("What is your favorite color? ").lower()

    if answer != "blue":          # Your security answer
        print("Security answer is incorrect.")
        return

    while True:
        new_password = input("Enter new lock password: ")
        confirm_password = input("Confirm new lock password: ")

        if new_password != confirm_password:
            print("Passwords do not match.")
            continue

        with open(LOCK_FILE, "w") as file:
            file.write(new_password)

        print("Lock password reset successfully.")
        break

with open("data/key.key", "rb") as f:
    KEY = f.read()

cipher = Fernet(KEY)

def encrypt_password(password):
    return cipher.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    return cipher.decrypt(encrypted_password.encode()).decode()

def get_userappname(): #This function prompts the user to enter a userappname and returns it.
    userappname = input("Enter userappname: ").capitalize()
    return userappname

def get_username(): #This function prompts the user to enter a username and returns it.
    username = input("Enter username: ")
    return username

def get_password_options(): #This function prompts the user to enter password options and returns them.
    try:
        length = int(input("Length: "))
    except ValueError:
        print("Invalid input")

    include_numbers = input("Include numbers? (y/n): ").lower()

    include_symbols = input("Include symbols? (y/n): ").lower()

    password_count = int(input("How many passwords do you want to generate? "))

    return length, include_numbers, include_symbols, password_count

def generate_password(length, include_numbers, include_symbols): #This function generates a password based on the specified options and returns it.

    characters = st.ascii_letters

    password = [
        rd.choice(st.ascii_uppercase),
        rd.choice(st.ascii_lowercase)
    ]
    minimum = 2

    if include_numbers == "y":
        minimum += 1

    if include_symbols == "y":
        minimum += 1

    if length < minimum:
        print("Password length too short.")

    if include_numbers == "y":
        characters += st.digits
        password.append(rd.choice(st.digits))

    if include_symbols == "y":
        characters += st.punctuation
        password.append(rd.choice(st.punctuation.replace("|", "")))

    while len(password) < length:
        password.append(rd.choice(characters.replace("|", "")))

    rd.shuffle(password)

    return "".join(password)

def check_strength(password):

    has_upper = False
    has_lower = False
    has_digit = False
    has_symbol = False

    for char in password:

        if char.isupper():
            has_upper = True

        elif char.islower():
            has_lower = True

        elif char.isdigit():
            has_digit = True

        elif char in st.punctuation:
            has_symbol = True

    if len(password) >= 12 and has_upper and has_lower and has_digit and has_symbol:
        return "Strong"

    elif len(password) >= 8 and has_upper and has_lower:
        return "Medium"

    else:
        return "Weak"

def save_to_file(userappname, username, password, strength):
    encrypted_password = encrypt_password(password)

    cursor.execute("""
    INSERT INTO passwords(app_name, username, password, strength)
    VALUES (?, ?, ?, ?)
    """, (userappname, username, encrypted_password, strength))
    print("Password saved successfully.")

    connection.commit()

def display_password(userappname, username, password, strength):

    print("\n----- Password Details -----")
    print("Userappname :", userappname)
    print("Username :", username)
    print("Password :", password)
    print("Strength :", strength)

def view_saved_passwords():


    cursor.execute("SELECT * FROM passwords")

    rows = cursor.fetchall()

    if not rows:
        print("No saved passwords.")
        return

    print("\n----- Saved Passwords -----\n")

    for row in rows:

        id, appname, username, password, strength = row
        password = decrypt_password(password)

        print(f"{id}. App Name : {appname}")
        print(f"   Username : {username}")
        print(f"   Password : {password}")
        print(f"   Strength : {strength}")
        print("-" * 25)

def update_saved_password():

    if not get_lock_password():
        print("Access denied.")
        return

    appname = input("Enter app name to update: ").lower()

    cursor.execute(
        "SELECT * FROM passwords WHERE LOWER(app_name)=?",
        (appname,)
    )

    row = cursor.fetchone()

    if row is None:
        print("App not found.")
        return

    print("\nGenerate a new password")

    length, include_numbers, include_symbols, _ = get_password_options()

    new_password = generate_password(
        length,
        include_numbers,
        include_symbols
    )
    encrypted_password = encrypt_password(new_password)

    strength = check_strength(new_password)

    cursor.execute("""
    UPDATE passwords
    SET password=?, strength=?
    WHERE LOWER(app_name)=?
    """, (encrypted_password, strength, appname))

    connection.commit()

    print("Password updated successfully.")

    display_password(row[1], row[2], new_password, strength)

def delete_saved_password():

    appname = input("Enter app name to delete: ").lower()

    cursor.execute(
        "SELECT * FROM passwords WHERE LOWER(app_name)=?",
        (appname,)
    )

    if cursor.fetchone() is None:
        print("App not found.")
        return

    cursor.execute(
        "DELETE FROM passwords WHERE LOWER(app_name)=?",
        (appname,)
    )

    connection.commit()

    print("Password deleted successfully.")

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

def ask_and_copy(password):
    choice = input("Copy password to clipboard? (y/n): ").lower()

    if choice == "yes" or choice == "y":
        copy_generated_password(password)
    else:
        print("-"*12)
        print("Copy skipped.")
        print("-"*12)


def copy_saved_password():

    if not get_lock_password():
        return

    cursor.execute(
        "SELECT id, app_name, username FROM passwords"
    )

    rows = cursor.fetchall()

    if not rows:
        print("No saved passwords.")
        return

    print("\n----- Saved Passwords -----")

    for row in rows:

        print(f"{row[0]}. App: {row[1]} | Username: {row[2]}")

    try:

        password_id = int(input("\nEnter password ID: "))

        cursor.execute(
            "SELECT password FROM passwords WHERE id=?",
            (password_id,)
        )

        result = cursor.fetchone()

        if result:

            password = decrypt_password(result[0])
            copy_generated_password(password)

        else:

            print("Invalid ID.")

    except ValueError:

        print("Please enter a valid number.")

def main():
   setup_lock()
   password = None
   while True:
        
        print("-"*18 + "\nPassword Generator\n" + "-"*18)
        print("1. Generate Password")
        print("2. View Saved Passwords")
        print("3. Update password")
        print("4. Delete Saved Password")
        print("5. Copy to clipboard")
        print("6. Copy saved passwords")
        print("7. Update lock")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ")

        if choice == "1":
            userappname = get_userappname()
            username = get_username()
            length, include_numbers, include_symbols, password_count = get_password_options()

            for _ in range(password_count):
                password = generate_password(length, include_numbers, include_symbols)
                strength = check_strength(password)
                display_password(userappname, username, password, strength)
                choice = input("Do you want to save password(y/n):").lower()
                if choice == 'y':
                    save_to_file(userappname, username, password, strength)
                else:
                    print("-"*38)
                    print("Thank you for using password generator")
                    print("-"*38)
                copy_generated_password(password)
        elif choice == "2":
            if get_lock_password():
                view_saved_passwords()
            else:
                print("Sorry you can't passwords!!")
        elif choice == "3":
            if get_lock_password():
                update_saved_password()
            else:
                print("Access denied")
        elif choice == "4":
            if get_lock_password():
                delete_saved_password()
            else:
                print("Can't delete password!!")
        
        elif choice == "5":
            if password is not None:
                ask_and_copy(password)
            else:
                print("Generate a password first.")
        elif choice == "6":
            if get_lock_password():
                copy_saved_password()
            else:
                print("Wrong password,can't copy passwords!!")    
        elif choice == "7":
            set_lock_password()
        elif choice == "8":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted.")
    finally:
        connection.close()