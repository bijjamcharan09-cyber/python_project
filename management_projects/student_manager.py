FILE_NAME= "student.txt"
def add_student(): #This function adds a new student record to the file
    name = input("Enter student name: ").capitalize() 
    num_subjects = int(input("How many subjects? ")) 
    record = name

    for i in range(num_subjects):
        print(f"\nSubject {i+1}") 
        subject = input("Enter subject name: ").capitalize() 
        marks = input("Enter marks: ") 
        credits = input("Enter credits for this subject: ") 
        record += "," + subject + ":" + marks + ":" + credits 

    with open(FILE_NAME, "a") as file: 
        file.write(record + "\n")

    print("-" * 20) 
    print("Student record saved!") 
    print("-" * 20) 

def view_students(): #This function reads and displays all student records from the file and handles the case where the file does not exist
    try:
        with open(FILE_NAME, "r") as file: 
            records = file.readlines()

            if not records: 
                print("\nNo student records found.")
                return

            print("\n" + "=" * 15)  
            print("STUDENT RECORDS") 
            print("=" * 15) 

            for student_no, line in enumerate(records, start=1): 
                data = line.strip().split(",")
                name = data[0]

                print(f"\nStudent {student_no}")
                print("-" * 15)
                print(f"Name : {name}\n")
                for i, subject_data in enumerate(data[1:], start=1): 
                    subject, marks, credits = subject_data.split(":")
                    print(f"{i}. Subject : {subject}")
                    print(f"   Marks   : {marks}")
                    print(f"   Credits : {credits}")

            print("\n" + "=" * 15)

    except FileNotFoundError:
        print("No records found.")

def calculate_average(): #This function calculates and displays the average marks for each student in the file. It handles the case where the file does not exist.
    try:
        with open(FILE_NAME, "r") as file:
            for line in file: 
                data = line.strip().split(",")
                name = data[0]
                total = 0
                count = 0
                for subject_data in data[1:]: 
                    subject, marks, credits = subject_data.split(":")
                    total += int(marks)
                    count += 1
                average = total / count
                print(f"{name}'s Average =", average)
    except FileNotFoundError:
        print("No records found.")

def clear_records(): #This function clears all student records from the file after confirming with the user. It handles the case where the file does not exist.
    confirm = input("Delete all records? (yes/no): ")
    if confirm.lower() == "yes": 
        with open(FILE_NAME, "w") as file:
            pass
        print("-" * 20)
        print("All records deleted.") 
        print("-" * 20)
    else: 
        print("Operation cancelled.")

def calculate_sgpa(): #This function calculates and displays the SGPA (Semester Grade Point Average) for each student in the file. It handles the case where the file does not exist.
    try:
        with open(FILE_NAME, "r") as file:

            for line in file: 
                data = line.strip().split(",")

                name = data[0]

                total_points = 0
                total_credits = 0

                for subject_data in data[1:]: 

                    subject, marks, credits = subject_data.split(":")

                    marks = int(marks)
                    credits = int(credits)

                    # Grade Point Calculation
                    if marks >= 90:
                        grade_point = 10
                    elif marks >= 80:
                        grade_point = 9
                    elif marks >= 70:
                        grade_point = 8
                    elif marks >= 60:
                        grade_point = 7
                    elif marks >= 50:
                        grade_point = 6
                    else:
                        grade_point = 0

                    total_points += grade_point * credits
                    total_credits += credits

                if total_credits > 0: 
                    sgpa = total_points / total_credits
                    print(f"{name}'s SGPA = {sgpa:.2f}")
                else: 
                    print(f"{name} has no subjects.")

    except FileNotFoundError:
        print("No records found.")

def delete_student(): #This function deletes specific student record from the file based on the student's name provided by the user. It handles the case where the file does not exist.
    name_to_delete = input("Enter student name to delete: ")

    try:
        with open(FILE_NAME, "r") as file:
            records = file.readlines()

        found = False

        with open(FILE_NAME, "w") as file: 
            for record in records:
                data = record.strip().split(",")

                if data[0].lower() != name_to_delete.lower():
                    file.write(record)
                else:
                    found = True

        if found: 
            print("-" * 20)
            print("Student record deleted successfully.")
            print("-" * 20)
        else:
            print("Student not found.")

    except FileNotFoundError:
        print("No records found.")

def total_students():#calculate total students
    try:
        with open(FILE_NAME, "r") as file:
            records = file.readlines()
            total = len(records) 
            if total == 0:
                print("No Student records found.")
            else:
                print(f"Total Students: {total}")
    except FileNotFoundError:
        print("No records found.")  

def search_student(): #This function searches for a specific student record in the file based on the student's name provided by the user. It handles the case where the file does not exist.
    name = input("Enter student name to search: ")

    try:
        with open(FILE_NAME, "r") as file:
            found = False

            for line in file:
                data = line.strip().split(",")

                if data[0].lower() == name.lower():
                    found = True
                    print("\nStudent Found")
                    print(" Name:", data[0])

                    for subject in data[1:]:
                        sub, marks, credits = subject.split(":")
                        print(f" Subject: {sub}\n Marks: {marks}\n Credits: {credits}")

            if not found: 
                print("Student not found.")

    except FileNotFoundError:
        print("No records found.")  

def update_student(): #This function updates a specific student record in the file based on the student's name provided by the user. It handles the case where the file does not exist.
    name_to_update = input("Enter student name to update: ").capitalize() #User input for the name of the student whose record needs to be updated. The input is capitalized to maintain consistency in the records.

    try:
        with open(FILE_NAME, "r") as file:
            records = file.readlines()

        found = False

        with open(FILE_NAME, "w") as file:
            for record in records:
                data = record.strip().split(",")

                if data[0].lower() == name_to_update.lower():
                    found = True

                    print("\nCurrent Record")
                    print("-" * 40)
                    print("Name:", data[0])

                    for i, subject_data in enumerate(data[1:], start=1):
                        subject, marks, credits = subject_data.split(":")
                        print(f"{i}. {subject} | Marks: {marks} | Credits: {credits}")
                    print("=" * 40)
                    print("\nEnter New Details")
                    print("=" * 40)

                    new_name = input("Enter new student name: ").capitalize() 

                    while True:
                        try:
                            num_subjects = int(input("Enter number of subjects: ")) 
                            if num_subjects > 0:
                                break
                            print("Enter at least one subject.")
                        except ValueError:
                            print("Enter a valid number.")

                    new_record = new_name 

                    for i in range(num_subjects):
                        print(f"\nSubject {i+1}")

                        subject = input("Subject Name : ").capitalize() 

                        while True:
                            try:
                                marks = int(input("Marks (0-100): ")) 
                                if 0 <= marks <= 100:
                                    break
                                print("Marks must be between 0 and 100.")
                            except ValueError:
                                print("Enter valid marks.")

                        while True:
                            try:
                                credits = int(input("Credits : ")) 
                                if credits > 0:
                                    break
                                print("Credits must be greater than 0.")
                            except ValueError:
                                print("Enter valid credits.")

                        new_record += f",{subject}:{marks}:{credits}"

                    file.write(new_record + "\n")

                else:
                    file.write(record)

        if found: 
            print("\nStudent record updated successfully.")
        else:
            print("\nStudent not found.")

    except FileNotFoundError:
        print("No records found.")

def student_ranking(): #This function calculates and displays the ranking of students based on their average marks. It handles the case where the file does not exist.
    try:
        with open(FILE_NAME, "r") as file:
            rankings = []

            for line in file:
                data = line.strip().split(",")
                name = data[0]

                total_marks = 0
                total_subjects = 0

                for subject_data in data[1:]:
                    subject, marks, credits = subject_data.split(":")
                    total_marks += int(marks)
                    total_subjects += 1

                average = total_marks / total_subjects
                rankings.append((name, average))

            rankings.sort(key=lambda x: x[1], reverse=True)

            print("\n" + "=" * 35)
            print("      STUDENT RANKING")
            print("=" * 35)
            print(f"{'Rank':<6}{'Name':<15}{'Average'}")
            print("-" * 35)

            for rank, (name, avg) in enumerate(rankings, start=1): 
                print(f"{rank:<6}{name:<15}{avg:.2f}")

    except FileNotFoundError:
        print("No records found.")

def topper_details(): #This function calculates and displays the details of the student with the highest average marks and the student with the highest SGPA (Semester Grade Point Average). It handles the case where the file does not exist.
    try:
        with open(FILE_NAME, "r") as file:

            highest_avg = -1 #Initialaziation of the highest average to -1.
            highest_sgpa = -1 #Initialization of the highest SGPA to -1.

            avg_topper = "" #Initialization of avg_topper to an empty string.
            sgpa_topper = "" #Initialization of sgpa_topper to an empty string.

            for line in file:
                data = line.strip().split(",")
                name = data[0]

                total_marks = 0 #Initialization of total_marks to 0.
                total_subjects = 0 #Initialization of total_subjects to 0.

                total_points = 0 #Initialization of total_points to 0.
                total_credits = 0 #Initialization of total_credits to 0.

                for subject_data in data[1:]:
                    subject, marks, credits = subject_data.split(":")

                    marks = int(marks)
                    credits = int(credits)

                    total_marks += marks #Calculates the total marks obtained by the student.
                    total_subjects += 1 #Calculates the total number of subjects taken by the student.
                    # Grade Point Calculation
                    if marks >= 90:
                        grade_point = 10
                    elif marks >= 80:
                        grade_point = 9
                    elif marks >= 70:
                        grade_point = 8
                    elif marks >= 60:
                        grade_point = 7
                    elif marks >= 50:
                        grade_point = 6
                    else:
                        grade_point = 0

                    total_points += grade_point * credits #Calculates total grade points earned by a student.
                    total_credits += credits #Calculates total credits earned by a student.

                average = total_marks / total_subjects #Calculates the average marks obtained.
                sgpa = total_points / total_credits #Calculates the sgpa of the student.

                if average > highest_avg: 
                    highest_avg = average
                    avg_topper = name

                if sgpa > highest_sgpa: 
                    highest_sgpa = sgpa
                    sgpa_topper = name

            print("\n" + "=" * 40) 
            print("           TOPPER DETAILS")
            print("=" * 40)
            print(f"Topper by Average : {avg_topper}")
            print(f"Average Marks     : {highest_avg:.2f}")
            print("-" * 40)
            print(f"Topper by SGPA    : {sgpa_topper}")
            print(f"SGPA              : {highest_sgpa:.2f}")
            print("=" * 40)

    except FileNotFoundError:
        print("No records found.")

def pass_fail_report(): #This function reports pass or fail
    try:
        with open(FILE_NAME, "r") as file:
            records = file.readlines()

            if not records:
                print("\nNo student records found.")
                return

            print("\n" + "=" * 45)
            print("           PASS / FAIL REPORT")
            print("=" * 45)

            for line in records:
                data = line.strip().split(",")
                name = data[0]

                failed_subjects = []

                for subject_data in data[1:]:
                    subject, marks, credits = subject_data.split(":")
                    marks = int(marks)

                    if marks < 50:
                        failed_subjects.append((subject, marks))

                print(f"\nStudent : {name}")

                if len(failed_subjects) == 0:
                    print("Status  : PASS")
                else:
                    print("Status  : FAIL")
                    print("Failed Subjects:")
                    for subject, marks in failed_subjects:
                        print(f"   • {subject} ({marks} Marks)")

            print("\n" + "=" * 45)

    except FileNotFoundError:
        print("No records found.")

def main(): #Main function that displays the menu and handles user input for various operations related to student records.
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
    try: #This line checks if the script is being run directly (not imported as a module) and executes the main function to start the program.
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted.")