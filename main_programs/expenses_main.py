import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database_files import expenses_db


def display_menu():
    print("\n===== Expense Tracker Menu =====")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Update Expense")
    print("4. Delete Expense")
    print("5. Search Expense")
    print("6. Total Expenses")
    print("7. Current Balance")
    print("8. Category Totals")
    print("9. Exit")


def add_expense():
    transaction = input("Transaction (Income/Expense): ")
    category = input("Category: ")
    amount = float(input("Amount: "))

    expenses_db.save_expense(
        transaction,
        category,
        amount
    )

    print("Expense added successfully.")


def view_expenses():
    expenses = expenses_db.fetch_expenses()

    if not expenses:
        print("\nNo expenses found.")
        return

    print("\nID\tTransaction\tCategory\tAmount\tDate\t\tTime")
    print("-" * 80)

    for expense in expenses:
        print(*expense, sep="\t")


def update_expense():
    expense_id = int(input("Enter Expense ID: "))
    transaction = input("Transaction (Income/Expense): ")
    category = input("Category: ")
    amount = float(input("Amount: "))
    date = input("Date (DD-MM-YYYY): ")
    time = input("Time (HH:MM:SS AM/PM): ")

    expenses_db.update_expense(
        expense_id,
        transaction,
        category,
        amount,
        date,
        time
    )

    print("Expense updated successfully.")


def delete_expense():
    view_expenses()

    expense_id = int(input("\nEnter Expense ID to delete: "))

    expenses_db.delete_expense(expense_id)

    print("Expense deleted successfully.")


def search_expense():
    category = input("Enter category to search: ")

    records = expenses_db.search_expense(category)

    if not records:
        print("No records found.")
        return

    print("\nID\tTransaction\tCategory\tAmount\tDate\t\tTime")
    print("-" * 80)

    for record in records:
        print(*record, sep="\t")


def total_expenses():
    total = expenses_db.calculate_total_expenses()
    print(f"\nTotal Expenses : ₹{total:.2f}")


def current_balance():
    income, expense, balance = expenses_db.calculate_current_balance()

    print("\n------ Current Balance ------")
    print(f"Total Income  : ₹{income:.2f}")
    print(f"Total Expense : ₹{expense:.2f}")
    print(f"Balance       : ₹{balance:.2f}")


def category_totals():
    rows = expenses_db.category_totals()

    print("\nCategory Totals")
    print("-" * 30)

    for category, total in rows:
        print(f"{category:<15} ₹{total:.2f}")


def main():
    expenses_db.initialize_database()

    while True:
        display_menu()

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_expense()

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            update_expense()

        elif choice == "4":
            delete_expense()

        elif choice == "5":
            search_expense()

        elif choice == "6":
            total_expenses()

        elif choice == "7":
            current_balance()

        elif choice == "8":
            category_totals()

        elif choice == "9":
            print("Thank you for using Expense Tracker.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()