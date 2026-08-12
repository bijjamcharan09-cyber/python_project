import sqlite3
db_file = "data/library.db"
def create_connection(db_file):
    """ create a database connection to the SQLite database specified by db_file """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn

def get_connection():
    """ Get a database connection to the SQLite database specified by db_file """
    conn = create_connection(db_file)
    return conn

def create_table(conn):
    """ create a table from the statement """
    try:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS books (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        author TEXT NOT NULL,
                        year INTEGER NOT NULL
                    );""")
    except sqlite3.Error as e:
        print(e)

def insert_book(conn, book):
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

def get_book_by_id(conn, book_id):
    """ Query a book by id """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE id=?", (book_id,))
    row = cursor.fetchone()
    return row

def issue_book(conn, book_id ):
    """ Issue a book by updating its issue status """
    sql = ''' UPDATE books
              SET issue = 'issued'
              WHERE id = ?'''
    cursor = conn.cursor()
    cursor.execute(sql, (book_id,))
    conn.commit()

def return_book(conn, book_id):
    """ Return a book by updating its issue status """
    sql = ''' UPDATE books
              SET issue = 'returned'
              WHERE id = ?'''
    cursor = conn.cursor()
    cursor.execute(sql, (book_id,))
    conn.commit()

def update_book(conn, book):
    """ Update a book in the books table """
    sql = ''' UPDATE books
              SET title = ? ,
                  author = ? ,
                  year = ? ,
              WHERE id = ?'''
    cursor = conn.cursor()
    cursor.execute(sql, book)
    conn.commit()

def delete_book(conn, book_id):
    """ Delete a book by book id """
    sql = 'DELETE FROM books WHERE id=?'
    cursor = conn.cursor()
    cursor.execute(sql, (book_id,))
    conn.commit()
    return cursor.rowcount