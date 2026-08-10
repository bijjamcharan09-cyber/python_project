import sqlite3
import os


# Database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "..", "data", "student_data.db")


# Connect to database
def get_connection():
    return sqlite3.connect(DB_NAME)


# Create database tables
def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            subject TEXT NOT NULL,
            marks INTEGER,
            credits INTEGER,
            FOREIGN KEY (student_id)
            REFERENCES students(student_id)
        )
    """)

    conn.commit()
    conn.close()


# Add student
def add_student(name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO students (name) VALUES (?)",
        (name,)
    )

    student_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return student_id


# Add subject
def add_subject(student_id, subject, marks, credits):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO subjects
        (student_id, subject, marks, credits)
        VALUES (?, ?, ?, ?)
    """, (student_id, subject, marks, credits))

    conn.commit()
    conn.close()


# Get all students
def get_students():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT student_id, name
        FROM students
    """)

    students = cursor.fetchall()

    conn.close()

    return students


# Get student by name
def get_student_by_name(name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT student_id, name
        FROM students
        WHERE name = ?
    """, (name,))

    student = cursor.fetchone()

    conn.close()

    return student


# Get subjects of a student
def get_subjects(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT subject, marks, credits
        FROM subjects
        WHERE student_id = ?
    """, (student_id,))

    subjects = cursor.fetchall()

    conn.close()

    return subjects


# Update student name
def update_student_name(student_id, new_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE students
        SET name = ?
        WHERE student_id = ?
    """, (new_name, student_id))

    conn.commit()
    conn.close()


# Delete student's subjects
def delete_student_subjects(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM subjects
        WHERE student_id = ?
    """, (student_id,))

    conn.commit()
    conn.close()


# Delete student
def delete_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM subjects
        WHERE student_id = ?
    """, (student_id,))

    cursor.execute("""
        DELETE FROM students
        WHERE student_id = ?
    """, (student_id,))

    conn.commit()
    conn.close()


# Delete all records
def clear_records():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM subjects")
    cursor.execute("DELETE FROM students")

    conn.commit()
    conn.close()


# Count students
def get_student_count():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM students
    """)

    count = cursor.fetchone()[0]

    conn.close()

    return count


# Get average marks of a student
def get_student_average(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT AVG(marks)
        FROM subjects
        WHERE student_id = ?
    """, (student_id,))

    average = cursor.fetchone()[0]

    conn.close()

    return average


# Get all student averages for ranking
def get_student_rankings():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT students.student_id,
               students.name,
               AVG(subjects.marks) AS average
        FROM students
        JOIN subjects
        ON students.student_id = subjects.student_id
        GROUP BY students.student_id
        ORDER BY average DESC
    """)

    rankings = cursor.fetchall()

    conn.close()

    return rankings


# Get topper
def get_topper():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT students.student_id,
               students.name,
               AVG(subjects.marks) AS average
        FROM students
        JOIN subjects
        ON students.student_id = subjects.student_id
        GROUP BY students.student_id
        ORDER BY average DESC
        LIMIT 1
    """)

    topper = cursor.fetchone()

    conn.close()

    return topper