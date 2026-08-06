from datetime import datetime
import sqlite3

DB_NAME = "data/expenses_tracker.db"

def connect_database():
    """
    Connects to the SQLite database.
    If the database does not exist, it will be created automatically.
    """
    connection = sqlite3.connect("data/expenses_tracker.db")
    return connection


def create_table():
    """
    Creates the expenses table if it does not already exist.
    """
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            [transaction] TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL
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


def save_expenses(transaction, category, amount):
    """
    Saves a new expense or income record into the SQLite database
    with the current date and time.
    """

    # Get current date and time
    current = datetime.now()
    current_date = current.strftime("%d-%m-%Y")
    current_time = current.strftime("%I:%M:%S %p")

    connection = connect_database()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO expenses (
                [transaction],
                category,
                amount,
                date,
                time
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            transaction,
            category,
            amount,
            current_date,
            current_time
        ))

        connection.commit()
        print("Expense saved successfully.")

    except sqlite3.Error as e:
        print("Database Error:", e)

    finally:
        connection.close()


def insert_expense(transaction, category, amount, date, time):
    """
    Inserts a new expense record into the database.
    """
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO expenses([transaction], category, amount, date, time)
        VALUES (?, ?, ?, ?, ?)
    """, (transaction, category, amount, date, time))

    connection.commit()
    connection.close()

    print("Expense added successfully.")


def fetch_expenses():
    """
    Retrieves all expense records from the database.
    """
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM expenses
    """)

    expenses = cursor.fetchall()

    connection.close()
    if not expenses:
        print("\n--- No Expenses ---")
    else:
        return expenses


def update_expense(expense_id, transaction, category, amount, date, time):
    """
    Updates an existing expense record in the database.
    """

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE expenses
        SET [transaction] = ?,
            category = ?,
            amount = ?,
            date = ?,
            time = ?
        WHERE id = ?
    """, (transaction, category, amount, date, time, expense_id))

    connection.commit()
    connection.close()

    print("Expense updated successfully.")


def display_menu():  # This function displays the main menu of the Expense Tracker application.
    print("\n--- Expense Tracker Menu ---")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Update Expense")
    print("4. Delete Expenses")
    print("5. Search Expense")
    print("6. Total Expenses")
    print("7. Current Balance")
    print("8. Category Totals")
    print("9. Exit")


def search_expense(category):
    """
    Searches expenses by category.
    """

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM expenses
        WHERE category = ?
    """, (category,))

    records = cursor.fetchall()

    connection.close()

    return records


def delete_expense(expense_id):
    """
    Deletes an expense from the database.
    """

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM expenses
        WHERE id = ?
    """, (expense_id,))

    connection.commit()
    connection.close()

    print("Expense deleted successfully.")


def calculate_total_expenses():
    """
    Calculates the total amount of all expenses.
    """

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT SUM(amount)
        FROM expenses
        WHERE transaction = 'Expense'
    """)

    total = cursor.fetchone()[0]

    connection.close()

    if total is None:
        total = 0

    print(f"Total Expenses : ₹{total:.2f}")


def calculate_current_balance():
    """
    Calculates total income, total expenses, and current balance.
    """

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT SUM(amount)
        FROM expenses
        WHERE transaction='Income'
    """)

    income = cursor.fetchone()[0]

    cursor.execute("""
        SELECT SUM(amount)
        FROM expenses
        WHERE transaction='Expense'
    """)

    expense = cursor.fetchone()[0]

    connection.close()

    income = income if income else 0
    expense = expense if expense else 0

    balance = income - expense

    print("\n------ Current Balance ------")
    print(f"Total Income   : ₹{income:.2f}")
    print(f"Total Expense  : ₹{expense:.2f}")
    print(f"Balance        : ₹{balance:.2f}")


def category_totals():
    """
    Displays total amount for each category.
    """

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT category,
               SUM(amount)
        FROM expenses
        GROUP BY category
    """)

    rows = cursor.fetchall()

    connection.close()

    print("\nCategory Totals")

    for category, total in rows:
        print(f"{category:<15} ₹{total:.2f}")


def main():  # Main function that serves as the entry point for the Expense Tracker application.
    create_table()
    expenses = fetch_expenses()  # Fetches existing expenses from the database.
    print("=" * 15)
    print("Expense Tracker")  # Formatting the title of the application.
    print("=" * 15)

    while True:
        display_menu()

        choice = input("Choose an option (1-9): ")

        match choice:
            case "1":

                transaction = input("Transaction (Income/Expense): ")

                category = input("Category: ")

                amount = float(input("Amount: "))

                save_expenses(
                    transaction,
                    category,
                    amount
                )
            case "2":
                fetch_expenses()
            case "3":
                    update_expense(expense_id=int(input("Enter expense ID to edit: ")),
                       transaction=input("Transaction (Income/Expense): "),
                       category=input("Category: "),
                       amount=float(input("Amount: ")),
                       date=input("Date (DD-MM-YYYY): "),
                       time=input("Time (HH:MM): "))
            case "4":
                delete_expense(expense_id=int(input("Enter expense ID to delete: ")))
            case "5":
                search_expense(category=input("Enter category to search: "))
            case "6":
                calculate_total_expenses()
            case "7":
                calculate_current_balance()
            case "8":
                category_totals()
            case "9":
                print("Exiting...")
                break
            case _:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":  # Checks if the script is being run directly (not imported) and calls the main function.
    try:
        main()
    except KeyboardInterrupt:  # Exception handling.
        print("\nProgram interrupted.")