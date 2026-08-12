import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)
from database_files import library_db
import ast
def add_book():
    book_title = input("Enter book title: ")
    book_author = input("Enter book author: ")
    book_year = input("Enter book year: ")
    library_db.insert_book(library_db.get_connection(), (book_title, book_author, book_year))
    print("Book added successfully.")

def view_books():
    books = library_db.get_all_books(library_db.get_connection())
    if not books:
        print("No books found.")
        return
    print("\nID\tTitle\tAuthor\tYear")
    print("-" * 40)
    for book in books:
        print(*book, sep="\t")

def search_book():
    book_id = input("Enter book ID to search: ")
    book = library_db.get_book_by_id(library_db.get_connection(), book_id)
    if not book:
        print("Book not found.")
        return
    print("\nID\tTitle\tAuthor\tYear")
    print("-" * 40)
    print(*book, sep="\t")

def issue_book():
    book_id = input("Enter book ID to issue: ")
    library_db.issue_book(library_db.get_connection(), book_id)
    print("Book issued successfully.")

def return_book():
    book_id = input("Enter book ID to return: ")
    library_db.return_book(library_db.get_connection(), book_id)
    print("Book returned successfully.")

def update_book():
    book_id = input("Enter book ID to update: ")
    book_title = input("Enter new book title: ")
    book_author = input("Enter new book author: ")
    book_year = input("Enter new book year: ")
    library_db.update_book(library_db.get_connection(), (book_title, book_author, book_year, book_id))
    print("Book updated successfully.")

def delete_book():
    book_id = input("Enter book ID to delete: ")
    library_db.delete_book(library_db.get_connection(), book_id)
    print("Book deleted successfully.")

def display_menu():
    print("1. Add Book")
    print("2. View Books")
    print("3. Search Book")
    print("4. Issue Book")
    print("5. Return Book")
    print("6. Update Book")
    print("7. Delete Book")
    print("8. Exit")

def main():
    conn = library_db.get_connection()
    library_db.create_table(conn)
    print("="*25 + "\nLibrary Management System\n" + "="*25)
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        if choice == '1':
            add_book()
        elif choice == '2':
            view_books()
        elif choice == '3':
            search_book()
        elif choice == '4':
            issue_book()
        elif choice == '5':
            return_book()
        elif choice == '6':
            update_book()
        elif choice == '7':
            delete_book()
        elif choice == '8':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main()
else:
    print("This script is intended to be run as the main program.")