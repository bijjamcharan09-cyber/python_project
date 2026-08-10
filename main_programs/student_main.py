import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database_files import student_db

def add_student():
    name = input("Enter student name: ").capitalize()

    student_id = student_db.add_student(name)
    num_subjects = int(input("How many subjects? "))

    for i in range(num_subjects):

        print(f"\nSubject {i+1}")

        subject = input("Subject Name : ").capitalize()
        marks = int(input("Marks : "))
        credits = int(input("Credits : "))
        student_db.add_subject(student_id, subject, marks, credits)

    print("-" * 25)
    print("Student Added Successfully")
    print("-" * 25)

def view_students():
    students = student_db.get_students()

    if not students:
        print("No students found.")
        return

    print("\nList of Students:")
    print("-" * 25)
    for student in students:
        print(f"ID: {student[0]}, Name: {student[1]}")
    print("-" * 25)

def view_student_details():
    name = input("Enter student name to view details: ").capitalize()
    student = student_db.get_student_by_name(name)

    if not student:
        print(f"No student found with name '{name}'.")
        return

    print("\nStudent Details:")
    print("-" * 25)
    print(f"ID: {student[0]}, Name: {student[1]}")
    subjects = student_db.get_subjects_by_student_id(student[0])

    if not subjects:
        print("No subjects found for this student.")
        return

    print("\nSubjects:")
    for subject in subjects:
        print(f"Subject: {subject[0]}, Marks: {subject[1]}, Credits: {subject[2]}")
    print("-" * 25)

def view_subjects():
    subjects = student_db.get_all_subjects()

    if not subjects:
        print("No subjects found.")
        return

    print("\nList of Subjects:")
    print("-" * 25)
    for subject in subjects:
        print(f"Student ID: {subject[0]}, Subject: {subject[1]}, Marks: {subject[2]}, Credits: {subject[3]}")
    print("-" * 25)

def update_student():
    name = input("Enter student name to update: ").capitalize()
    student = student_db.get_student_by_name(name)

    if not student:
        print(f"No student found with name '{name}'.")
        return

    new_name = input("Enter new name (leave blank to keep current): ").capitalize()
    student_id = input("Enter student ID to update: ")
    if new_name:
        student_db.update_student_name(student_id, new_name)
        print("Student name updated successfully.")
    else:
        print("No changes made.")

def delete_student():
    name = input("Enter student name to delete: ").capitalize()
    student = student_db.get_student_by_name(name)

    if not student:
        print(f"No student found with name '{name}'.")
        return

    confirm = input(f"Are you sure you want to delete student '{name}'? (y/n): ").lower()
    if confirm == 'y':
        student_id = input("Enter student ID to delete: ")
        student_db.delete_student_subjects(student_id)
        student_db.delete_student(student_id)
        print("Student and their subjects deleted successfully.")
    else:
        print("Deletion cancelled.")

def clear_records():
    confirm = input("Are you sure you want to clear all records? (y/n): ").lower()
    if confirm == 'y':
        student_db.clear_records()
        print("All records cleared successfully.")
    else:
        print("Operation cancelled.")

def student_count():
    count = student_db.get_student_count()
    print(f"Total number of students: {count}")

def student_average_marks():
    name = input("Enter student name to calculate average marks: ").capitalize()
    student = student_db.get_student_by_name(name)

    if not student:
        print(f"No student found with name '{name}'.")
        return

    subjects = student_db.get_subjects_by_student_id(student[0])

    if not subjects:
        print("No subjects found for this student.")
        return

    total_marks = sum(subject[1] for subject in subjects)
    average_marks = total_marks / len(subjects)

    print(f"Average marks for {name}: {average_marks:.2f}")

def get_student_rankings():
    rankings = student_db.get_student_rankings()

    if not rankings:
        print("No students found.")
        return

    print("\nStudent Rankings:")
    print("-" * 25)
    for rank, (student_id, name, average) in enumerate(rankings, start=1):
        print(f"Rank: {rank}, ID: {student_id}, Name: {name}, Average Marks: {average:.2f}")
    print("-" * 25)

def get_topper():
    topper = student_db.get_topper()

    if not topper:
        print("No students found.")
        return

    print("\nTopper:")
    print("-" * 25)
    print(f"ID: {topper[0]}, Name: {topper[1]}, Average Marks: {topper[2]:.2f}")
    print("-" * 25)

def menu():
        print("="*25 + "\nStudent Management System\n" + "="*25)
        print("1. Add Student")
        print("2. View Students")
        print("3. View Student Details")
        print("4. View Subjects")
        print("5. Update Student")
        print("6. Delete Student")
        print("7. Clear All Records")
        print("8. Count Students")
        print("9. Calculate Average Marks")
        print("10. Get Student Rankings")
        print("11. Get Topper")
        print("12. Exit")

def main():
    menu()
    while True:
        choice = input("Enter your choice (1-12): ")

        if choice == '1':
            add_student()
        elif choice == '2':
            view_students()
        elif choice == '3':
            view_student_details()
        elif choice == '4':
            view_subjects()
        elif choice == '5':
            update_student()
        elif choice == '6':
            delete_student()
        elif choice == '7':
            clear_records()
        elif choice == '8':
            student_count()
        elif choice == '9':
            student_average_marks()
        elif choice == '10':
            get_student_rankings()
        elif choice == '11':
            get_topper()
        elif choice == '12':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main()
else:
    print("This module is intended to be run as a standalone program.")