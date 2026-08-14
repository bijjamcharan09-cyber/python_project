import sqlite3
import os

DB_NAME = "data/books.db"


def get_connection():
    # Make sure the data directory exists
    os.makedirs(os.path.dirname(DB_NAME), exist_ok=True)
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER NOT NULL,
            issue TEXT NOT NULL DEFAULT 'returned'
        )
    """)

    conn.commit()
    conn.close()


def insert_book_db(conn, book):
    """Insert a new book into the books table."""
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO books (title, author, year)
        VALUES (?, ?, ?)
    """, book)

    conn.commit()
    return cursor.lastrowid


def get_all_books(conn):
    """Query all rows in the books table."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    return cursor.fetchall()


def search_book_by_id(conn, book_id):
    """Query a book by ID."""
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM books WHERE id = ?",
        (book_id,)
    )

    return cursor.fetchone()


def issue_book_db(conn, book_id):
    """Issue a book."""
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE books
        SET issue = 'issued'
        WHERE id = ?
    """, (book_id,))

    conn.commit()
    return cursor.rowcount


def return_book_db(conn, book_id):
    """Return a book."""
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE books
        SET issue = 'returned'
        WHERE id = ?
    """, (book_id,))

    conn.commit()
    return cursor.rowcount


def update_book_db(conn, book):
    """Update a book in the books table."""
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE books
        SET title = ?,
            author = ?,
            year = ?
        WHERE id = ?
    """, book)

    conn.commit()
    return cursor.rowcount


def delete_book_db(conn, book_id):
    """Delete a book by book ID."""
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM books WHERE id = ?",
        (book_id,)
    )

    conn.commit()
    return cursor.rowcount


# -------------------------
# Menu / User Functions
# -------------------------

def add_book(conn):
    book_title = input("Enter book title: ")
    book_author = input("Enter book author: ")
    book_year = input("Enter book year: ")

    insert_book_db(
        conn,
        (book_title, book_author, book_year)
    )

    print("Book added successfully.")


def view_books(conn):
    books = get_all_books(conn)

    if not books:
        print("No books found.")
        return

    print("\nID\tTitle\tAuthor\tYear\tStatus")
    print("-" * 60)

    for book in books:
        print(*book, sep="\t")


def search_book(conn):
    book_id = input("Enter book ID to search: ")

    book = search_book_by_id(conn, book_id)

    if not book:
        print("Book not found.")
        return

    print("\nID\tTitle\tAuthor\tYear\tStatus")
    print("-" * 60)
    print(*book, sep="\t")


def issue_book(conn):
    book_id = input("Enter book ID to issue: ")

    result = issue_book_db(conn, book_id)

    if result == 0:
        print("Book not found.")
        return

    print("Book issued successfully.")


def return_book(conn):
    book_id = input("Enter book ID to return: ")

    result = return_book_db(conn, book_id)

    if result == 0:
        print("Book not found.")
        return

    print("Book returned successfully.")


def update_book(conn):
    book_id = input("Enter book ID to update: ")
    book_title = input("Enter new book title: ")
    book_author = input("Enter new book author: ")
    book_year = input("Enter new book year: ")

    result = update_book_db(
        conn,
        (book_title, book_author, book_year, book_id)
    )

    if result == 0:
        print("Book not found.")
        return

    print("Book updated successfully.")


def delete_book(conn):
    book_id = input("Enter book ID to delete: ")

    result = delete_book_db(conn, book_id)

    if result == 0:
        print("Book not found.")
        return

    print("Book deleted successfully.")


# -------------------------
# Main Program
# -------------------------

def main():
    conn = get_connection()

    while True:
        print("\n" + "=" * 25)
        print("Library Management System")
        print("=" * 25)

        print("1. Add Book")
        print("2. View Books")
        print("3. Search Book")
        print("4. Issue Book")
        print("5. Return Book")
        print("6. Delete Book")
        print("7. Update Book")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_book(conn)

        elif choice == "2":
            view_books(conn)

        elif choice == "3":
            search_book(conn)

        elif choice == "4":
            issue_book(conn)

        elif choice == "5":
            return_book(conn)

        elif choice == "6":
            delete_book(conn)

        elif choice == "7":
            update_book(conn)

        elif choice == "8":
            print("Thank you!")
            conn.close()
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    create_table()
    main()
else:
    print("Program interupted")