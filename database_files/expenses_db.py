from datetime import datetime
import sqlite3

DB_NAME = "data/expenses_tracker.db"


def connect_database():
    """Connect to the SQLite database."""
    return sqlite3.connect(DB_NAME)


def create_table():
    """Create the expenses table if it does not exist."""
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
    """Initialize the database."""
    create_table()
    print("Database initialized successfully.")


def save_expense(transaction, category, amount):
    """Save a new expense/income."""
    current = datetime.now()
    current_date = current.strftime("%d-%m-%Y")
    current_time = current.strftime("%I:%M:%S %p")

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO expenses
        ([transaction], category, amount, date, time)
        VALUES (?, ?, ?, ?, ?)
    """, (
        transaction,
        category,
        amount,
        current_date,
        current_time
    ))

    connection.commit()
    connection.close()


def fetch_expenses():
    """Return all expense records."""
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM expenses")

    expenses = cursor.fetchall()

    connection.close()

    return expenses


def update_expense(expense_id, transaction, category,
                   amount, date, time):
    """Update an expense."""
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE expenses
        SET
            [transaction]=?,
            category=?,
            amount=?,
            date=?,
            time=?
        WHERE id=?
    """, (
        transaction,
        category,
        amount,
        date,
        time,
        expense_id
    ))

    connection.commit()
    connection.close()


def delete_expense(expense_id):
    """Delete an expense."""
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM expenses
        WHERE id=?
    """, (expense_id,))

    connection.commit()
    connection.close()


def search_expense(category):
    """Search expenses by category."""
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM expenses
        WHERE category=?
    """, (category,))

    records = cursor.fetchall()

    connection.close()

    return records


def calculate_total_expenses():
    """Return total expense amount."""
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT SUM(amount)
        FROM expenses
        WHERE [transaction]='Expense'
    """)

    total = cursor.fetchone()[0]

    connection.close()

    return total if total else 0


def calculate_current_balance():
    """Return income, expense and balance."""
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT SUM(amount)
        FROM expenses
        WHERE [transaction]='Income'
    """)
    income = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT SUM(amount)
        FROM expenses
        WHERE [transaction]='Expense'
    """)
    expense = cursor.fetchone()[0] or 0

    connection.close()

    balance = income - expense

    return income, expense, balance


def category_totals():
    """Return total amount for each category."""
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows