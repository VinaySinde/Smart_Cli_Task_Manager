
from task_manager import TaskManager


def display_menu():
    print("\n" + "=" * 42)
    print("       SMART CLI TASK MANAGER")
    print("=" * 42)
    print("1.  Add Task")
    print("2.  View All Tasks")
    print("3.  Update Task")
    print("4.  Delete Task")
    print("5.  Mark Task Completed")
    print("6.  Search Tasks")
    print("7.  View Overdue Tasks")
    print("8.  Task Statistics")
    print("9.  Filter Tasks")
    print("0.  Exit")
    print("=" * 42)


def main():
    manager = TaskManager()

    actions = {
        "1": manager.add_task,
        "2": manager.view_tasks,
        "3": manager.update_task,
        "4": manager.delete_task,
        "5": manager.complete_task,
        "6": manager.search_tasks,
        "7": manager.view_overdue_tasks,
        "8": manager.statistics,
        "9": manager.filter_tasks
    }

    print("Welcome to Smart CLI Task Manager!")

    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "0":
            print("Thank you for using Smart CLI Task Manager!")
            break

        action = actions.get(choice)

        if action:
            try:
                action()
            except (OSError, ValueError) as error:
                print(f"An error occurred: {error}")
        else:
            print("Invalid choice. Please choose an option from the menu.")


if __name__ == "__main__":
    main()
