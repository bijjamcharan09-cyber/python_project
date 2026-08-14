import ast
import sqlite3

DB_NAME = "data/books.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS books (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        author TEXT NOT NULL,
                        year INTEGER NOT NULL
                    );""")

def insert_book_db(conn, book):
    """ Insert a new book into the books table """
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
        INSERT INTO books (title, author, year)
        VALUES (?, ?, ?)
    """, book)
    conn.commit()
    return cursor.lastrowid

def get_all_books(conn):
    """ Query all rows in the books table """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    return rows

def search_book_by_id(conn, book_id):
    """ Query a book by id """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE id=?", (book_id,))
    row = cursor.fetchone()
    return row

def issue_book_db(conn, book_id ):
    """ Issue a book by updating its issue status """
    sql = ''' UPDATE books
              SET issue = 'issued'
              WHERE id = ?'''
    cursor = conn.cursor()
    cursor.execute(sql, (book_id,))
    conn.commit()

def return_book_db(conn, book_id):
    """ Return a book by updating its issue status """
    sql = ''' UPDATE books
              SET issue = 'returned'
              WHERE id = ?'''
    cursor = conn.cursor()
    cursor.execute(sql, (book_id,))
    conn.commit()

def update_book_db(conn, book):
    """ Update a book in the books table """
    sql = ''' UPDATE books
              SET title = ? ,
                  author = ? ,
                  year = ? ,
              WHERE id = ?'''
    cursor = conn.cursor()
    cursor.execute(sql, book)
    conn.commit()

def delete_book_db(conn, book_id):
    """ Delete a book by book id """
    sql = 'DELETE FROM books WHERE id=?'
    cursor = conn.cursor()
    cursor.execute(sql, (book_id,))
    conn.commit()
    return cursor.rowcount

def add_book():
    book_title = input("Enter book title: ")
    book_author = input("Enter book author: ")
    book_year = input("Enter book year: ")
    insert_book_db((book_title, book_author, book_year))
    print("Book added successfully.")

def view_books():
    books = get_all_books()
    if not books:
        print("No books found.")
        return
    print("\nID\tTitle\tAuthor\tYear")
    print("-" * 40)
    for book in books:
        print(*book, sep="\t")

def search_book():
    book_id = input("Enter book ID to search: ")
    book = search_book_by_id(book_id)
    if not book:
        print("Book not found.")
        return
    print("\nID\tTitle\tAuthor\tYear")
    print("-" * 40)
    print(*book, sep="\t")

def issue_book():
    book_id = input("Enter book ID to issue: ")
    issue_book(book_id)
    print("Book issued successfully.")

def return_book():
    book_id = input("Enter book ID to return: ")
    return_book(book_id)
    print("Book returned successfully.")

def update_book():
    book_id = input("Enter book ID to update: ")
    book_title = input("Enter new book title: ")
    book_author = input("Enter new book author: ")
    book_year = input("Enter new book year: ")
    update_book((book_title, book_author, book_year, book_id))
    print("Book updated successfully.")

def delete_book():
    book_id = input("Enter book ID to delete: ")
    delete_book(book_id)
    print("Book deleted successfully.")


def main():
    conn = get_connection()
    get_all_books(conn)

    while True:

        print("="*25 + "\nLibrary Management System\n" + "="*25)
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
            insert_book_db(add_book())

        elif choice == "2":
            get_all_books(view_books())

        elif choice == "3":
            search_book_by_id(search_book())

        elif choice == "4":
            issue_book_db(issue_book())

        elif choice == "5":
            return_book_db(return_book())

        elif choice == "6":
            delete_book_db(delete_book())

        elif choice == "7":
            update_book_db(update_book)

        elif choice == "8":
            print("Thank you!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    create_table()
    main()
else:
    print("Program interupted(EX: ctrl + v)")