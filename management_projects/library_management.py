import ast

FILENAME = "data/books.txt"


def load_books():
    books = []

    try:
        with open(FILENAME, "r") as file:
            for line in file:
                books.append(ast.literal_eval(line.strip()))
    except FileNotFoundError:
        pass

    return books


def save_books(books):
    with open(FILENAME, "w") as file:
        for book in books:
            file.write(str(book) + "\n")


def add_book(books):
    title = input("Enter book title: ").capitalize()
    author = input("Enter author name: ").capitalize()

    book = {
        "title": title,
        "author": author,
        "issued": False
    }

    books.append(book)
    save_books(books)
    print("-"*29)
    print("Book added successfully.")
    print("-"*29)


def view_books(books):
    print("-"*29)
    if not books:
        print("No books available.")
        print("-"*29)
        return

    for i, book in enumerate(books, start=1):
        status = "Issued" if book["issued"] else "Available"
        print(f"\nBook {i}")
        print(f"Title : {book['title']}")
        print(f"Author: {book['author']}")
        print(f"Status: {status}")
        print("-"*29)



def search_book(books):
    title = input("Enter book title: ").capitalize()
    print("-"*29)

    found = False

    for book in books:
        if book["title"] == title:
            status = "Issued" if book["issued"] else "Available"

            print("Book Found")
            print(f"Title : {book['title']}")
            print(f"Author: {book['author']}")
            print(f"Status: {status}")
            print("-"*29)


            found = True

    if not found:
        print("-"*29)
        print("Book not found.")
        print("-"*29)



def issue_book(books):
    title = input("Enter book title to issue: ").capitalize()

    for book in books:
        if book["title"] == title:

            if book["issued"]:
                print("Book is already issued.")
                print("-"*29)
            else:
                book["issued"] = True
                save_books(books)
                print("-"*29)
                print("Book issued successfully.")
                print("-"*29)

            return
    print("-"*29)
    print("Book not found.")
    print("-"*29)


def return_book(books):
    title = input("Enter book title to return: ").capitalize()
    print("-"*30)

    for book in books:
        if book["title"] == title:

            if not book["issued"]:
                print("Book is already available.")
                print("-"*30)
            else:
                book["issued"] = False
                save_books(books)
                print("Book returned successfully.")
                print("-"*30)

            return

    print("Book not found.")


def delete_book(books):
    title = input("Enter book title to delete: ").capitalize()
    print("-"*29)

    for book in books:
        if book["title"] == title:
            books.remove(book)
            save_books(books)
            print("Book deleted successfully.")
            print("-"*29)
            return

    print("Book not found.")
    print("-"*29)

def update_book(books):
    old_title = input("Enter the book title to update: ").capitalize()
    print("-" * 29)

    for book in books:
        if book["title"] == old_title:

            print("Current Details")
            print(f"Title : {book['title']}")
            print(f"Author: {book['author']}")
            print("-" * 29)

            new_title = input("Enter new title (press Enter to keep same): ").capitalize()
            new_author = input("Enter new author (press Enter to keep same): ").capitalize()

            if new_title:
                book["title"] = new_title

            if new_author:
                book["author"] = new_author

            save_books(books)

            print("-" * 29)
            print("Book updated successfully.")
            print("-" * 29)
            return

    print("Book not found.")
    print("-" * 29)

def main():
    books = load_books()

    while True:

        print("\n===== Library Management System =====")
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
            add_book(books)

        elif choice == "2":
            view_books(books)

        elif choice == "3":
            search_book(books)

        elif choice == "4":
            issue_book(books)

        elif choice == "5":
            return_book(books)

        elif choice == "6":
            delete_book(books)

        elif choice == "7":
            update_book(books)

        elif choice == "8":
            print("Thank you!")
            break

        else:
            print("Invalid choice.")


main()