import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "..", "data", "student.db")

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects(
        subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject TEXT NOT NULL,
        marks INTEGER,
        credits INTEGER,
        FOREIGN KEY(student_id) REFERENCES students(student_id)
    )
    """)

    conn.commit()
    conn.close()

def add_student():

    conn = get_connection()
    cursor = conn.cursor()

    name = input("Enter student name: ").capitalize()

    cursor.execute(
        "INSERT INTO students(name) VALUES(?)",
        (name,)
    )

    student_id = cursor.lastrowid

    num_subjects = int(input("How many subjects? "))

    for i in range(num_subjects):

        print(f"\nSubject {i+1}")

        subject = input("Subject Name : ").capitalize()
        marks = int(input("Marks : "))
        credits = int(input("Credits : "))

        cursor.execute("""
        INSERT INTO subjects(student_id,subject,marks,credits)
        VALUES(?,?,?,?)
        """, (student_id, subject, marks, credits))

    conn.commit()
    conn.close()

    print("-" * 25)
    print("Student Added Successfully")
    print("-" * 25)

def view_students():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    if not students:
        print("No student records found.")
        conn.close()
        return

    print("=" * 40)
    print("STUDENT RECORDS")
    print("=" * 40)

    for student in students:

        student_id = student[0]
        name = student[1]

        print(f"\nName : {name}")

        cursor.execute("""
        SELECT subject,marks,credits
        FROM subjects
        WHERE student_id=?
        """, (student_id,))

        subjects = cursor.fetchall()

        for i, sub in enumerate(subjects, start=1):

            print(f"{i}. Subject : {sub[0]}")
            print(f"   Marks   : {sub[1]}")
            print(f"   Credits : {sub[2]}")

    conn.close()

def search_student():

    name = input("Enter student name to search: ").capitalize()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT student_id, name FROM students WHERE name = ?",
        (name,)
    )

    student = cursor.fetchone()

    if student:

        student_id = student[0]

        print("\nStudent Found")
        print("-" * 30)
        print("Name :", student[1])

        cursor.execute("""
        SELECT subject, marks, credits
        FROM subjects
        WHERE student_id = ?
        """, (student_id,))

        subjects = cursor.fetchall()

        for i, subject in enumerate(subjects, start=1):
            print(f"\n{i}. Subject : {subject[0]}")
            print(f"   Marks   : {subject[1]}")
            print(f"   Credits : {subject[2]}")

    else:
        print("Student not found.")

    conn.close()

def update_student():

    name = input("Enter student name to update: ").capitalize()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT student_id FROM students WHERE name=?",
        (name,)
    )

    student = cursor.fetchone()

    if not student:
        print("Student not found.")
        conn.close()
        return

    student_id = student[0]

    new_name = input("Enter new student name: ").capitalize()

    cursor.execute(
        "UPDATE students SET name=? WHERE student_id=?",
        (new_name, student_id)
    )

    cursor.execute(
        "DELETE FROM subjects WHERE student_id=?",
        (student_id,)
    )

    num_subjects = int(input("Enter number of subjects: "))

    for i in range(num_subjects):

        print(f"\nSubject {i+1}")

        subject = input("Subject Name : ").capitalize()
        marks = int(input("Marks : "))
        credits = int(input("Credits : "))

        cursor.execute("""
        INSERT INTO subjects(student_id, subject, marks, credits)
        VALUES(?,?,?,?)
        """, (student_id, subject, marks, credits))

    conn.commit()
    conn.close()

    print("Student record updated successfully.")

def delete_student():

    name = input("Enter student name to delete: ").capitalize()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT student_id FROM students WHERE name=?",
        (name,)
    )

    student = cursor.fetchone()

    if not student:
        print("Student not found.")
        conn.close()
        return

    student_id = student[0]

    cursor.execute(
        "DELETE FROM subjects WHERE student_id=?",
        (student_id,)
    )

    cursor.execute(
        "DELETE FROM students WHERE student_id=?",
        (student_id,)
    )

    conn.commit()
    conn.close()

    print("Student deleted successfully.")

def calculate_average():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT student_id, name FROM students")
    students = cursor.fetchall()

    if not students:
        print("No student records found.")
        conn.close()
        return

    print("\nAverage Marks")
    print("-" * 30)

    for student_id, name in students:

        cursor.execute("""
        SELECT AVG(marks)
        FROM subjects
        WHERE student_id=?
        """, (student_id,))

        average = cursor.fetchone()[0]

        print(f"{name}'s Average = {average:.2f}")

    conn.close()

def clear_records():

    confirm = input("Delete all records? (yes/no): ")

    if confirm.lower() != "yes":
        print("Operation cancelled.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM subjects")
    cursor.execute("DELETE FROM students")

    conn.commit()
    conn.close()

    print("All records deleted successfully.")

def calculate_sgpa():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT student_id, name FROM students")
    students = cursor.fetchall()

    if not students:
        print("No student records found.")
        conn.close()
        return

    print("\nSGPA REPORT")
    print("-" * 30)

    for student_id, name in students:

        cursor.execute("""
        SELECT marks, credits
        FROM subjects
        WHERE student_id=?
        """, (student_id,))

        subjects = cursor.fetchall()

        total_points = 0
        total_credits = 0

        for marks, credits in subjects:

            if marks >= 90:
                grade = 10
            elif marks >= 80:
                grade = 9
            elif marks >= 70:
                grade = 8
            elif marks >= 60:
                grade = 7
            elif marks >= 50:
                grade = 6
            else:
                grade = 0

            total_points += grade * credits
            total_credits += credits

        sgpa = total_points / total_credits

        print(f"{name}'s SGPA = {sgpa:.2f}")

    conn.close()

def total_students():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")

    total = cursor.fetchone()[0]

    print(f"Total Students : {total}")

    conn.close()

def student_ranking():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT students.name,
           AVG(subjects.marks) AS average
    FROM students
    JOIN subjects
    ON students.student_id = subjects.student_id
    GROUP BY students.student_id
    ORDER BY average DESC
    """)

    rankings = cursor.fetchall()

    if not rankings:
        print("No student records found.")
        conn.close()
        return

    print("=" * 35)
    print("STUDENT RANKING")
    print("=" * 35)

    for rank, (name, average) in enumerate(rankings, start=1):
        print(f"{rank}. {name}  {average:.2f}")

    conn.close()

def topper_details():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT students.name,
           AVG(subjects.marks) AS average
    FROM students
    JOIN subjects
    ON students.student_id = subjects.student_id
    GROUP BY students.student_id
    ORDER BY average DESC
    LIMIT 1
    """)

    topper = cursor.fetchone()

    if topper:
        print("\nTOPPER DETAILS")
        print("-" * 30)
        print("Name :", topper[0])
        print(f"Average : {topper[1]:.2f}")

    else:
        print("No student records found.")

    conn.close()

def pass_fail_report():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT student_id, name FROM students")

    students = cursor.fetchall()

    if not students:
        print("No student records found.")
        conn.close()
        return

    print("=" * 40)
    print("PASS / FAIL REPORT")
    print("=" * 40)

    for student_id, name in students:

        cursor.execute("""
        SELECT subject, marks
        FROM subjects
        WHERE student_id=?
        """, (student_id,))

        subjects = cursor.fetchall()

        failed = []

        for subject, marks in subjects:

            if marks < 50:
                failed.append((subject, marks))

        print(f"\nStudent : {name}")

        if not failed:
            print("Status : PASS")
        else:
            print("Status : FAIL")
            print("Failed Subjects:")

            for subject, marks in failed:
                print(f"• {subject} ({marks})")

    conn.close()

def main():
    print("=" *15 + "\nStudent Manager\n" +"=" *15)
    while True:
        print("_" *16 + "\n      MENU\n" +"*" *16)
        print("1. Add Student")
        print("2. View Students")
        print("3. Calculate Average")
        print("4. Clear Records")
        print("5. Calculate SGPA")
        print("6. Delete Student Record")
        print("7. Total Students")
        print("8. Search Student")
        print("9. Update Student Record")
        print("10. Student Ranking")
        print("11. Topper Details")
        print("12. Pass/Fail Report")
        print("13. Exit")

        choice = input("Enter your choice(1-13): ")

        if choice == "1":
            add_student()

        elif choice == "2":
            view_students()
        elif choice == "3":
            calculate_average()
        elif choice == "4":
            clear_records()
        elif choice == "5":
            calculate_sgpa()
        elif choice == "6":
            delete_student()
        elif choice == "7":
            total_students()
        elif choice == "8":
            search_student()
        elif choice == "9":
            update_student()
        elif choice == "10":
            student_ranking()
        elif choice == "11":
            topper_details()
        elif choice == "12":
            pass_fail_report()
        elif choice == "13":
            print("Program Ended.")
            break
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    try:
        create_database()
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted.")