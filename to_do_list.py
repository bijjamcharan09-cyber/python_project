from datetime import datetime
filename = "data/to_do.txt"
def display_menu():  # This function displays the main menu options to the user.
    print("\n===== TO-DO LIST =====")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Delete Tasks")
    print("4. Exit")

def load_tasks(filename="data/to_do.txt"): #This function loads all the previous tasks in a file.
    tasks = []

    try:
        with open(filename, "r") as file:
            for line in file:
                task, date, time = line.strip().split(",")

                tasks.append({
                    "task": task,
                    "date": date,
                    "time": time
                })
    except FileNotFoundError:
        pass
    except IOError:
        print("Error loading tasks.")

    return tasks

def add_task(tasks):  # This function prompts the user to enter a new task.
    task = input("Enter a new task: ").strip().capitalize()

    if task == "":
        print("Task cannot be empty.")
        return

    now = datetime.now()

    tasks.append({
        "task": task,
        "date": now.strftime("%d-%m-%Y"),
        "time": now.strftime("%I:%M:%S %p")
    })

    print("Task added successfully.")

def view_tasks(tasks):  # This function displays all the tasks.

    if not tasks:
        print("\nNo tasks available.")
        return

    print("\n----- YOUR TASKS -----")

    for index, task in enumerate(tasks, start=1):
        print(
            f"{index}. Task = {task['task']}\n   "
            f"Date = {task['date']}\n   "
            f"Time = {task['time']}"
        )


def save_tasks(tasks, filename="data/to_do.txt"): #This function saves the tasks into a file and uses exception handling.

    try:
        with open(filename, "w") as file:

            for task in tasks:

                file.write(
                    f"{task['task']},{task['date']},{task['time']}\n"
                )

    except IOError:
        print("Error saving tasks.")

def clear_tasks(tasks, filename="data/to_do.txt"): # This function clears all the tasks from the list and the file.
    confirm = input("Are you sure? (yes/no): ").lower()
    if confirm == "yes":
        tasks.clear()
        open(filename, "w").close()
        print("All tasks cleared!")
    else:
        print("Operation cancelled.")


def main():  # This is the main function.
    tasks = load_tasks()
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()
        match choice:
             case "1":
                 add_task(tasks)
                 save_tasks(tasks,filename="data/to_do.txt")
             case "2":
                 view_tasks(tasks)
             case "3":
                 clear_tasks(tasks,filename = "data/to_do.txt")
             case "4":
                 print("Exiting.")
                 break
             case "_":
                 print("Please enter a valid choice.")

if __name__ == "__main__":
    main()