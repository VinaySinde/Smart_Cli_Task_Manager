
from datetime import date, datetime


def get_due_date():
    """Ask for an optional due date in YYYY-MM-DD format."""
    while True:
        value = input("Due date (YYYY-MM-DD, or press Enter to skip): ").strip()

        if not value:
            return None

        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print("Invalid date. Example: 2026-10-15")


def get_priority():
    """Get a valid task priority."""
    while True:
        priority = input("Priority (high/medium/low): ").strip().lower()

        if priority in ("high", "medium", "low"):
            return priority

        print("Please enter high, medium, or low.")


def get_task_status(task):
    """Calculate the current task status."""
    if task["completed"]:
        return "COMPLETED"

    due_date = task.get("due_date")

    if due_date:
        try:
            if date.fromisoformat(due_date) < date.today():
                return "OVERDUE"
        except ValueError:
            pass

    return "PENDING"


def print_task(task):
    """Display one task."""
    print("-" * 60)
    print(f"ID       : {task['id']}")
    print(f"Title    : {task['title']}")
    print(f"Details  : {task.get('description') or 'None'}")
    print(f"Priority : {task['priority'].upper()}")
    print(f"Due date : {task.get('due_date') or 'None'}")
    print(f"Status   : {get_task_status(task)}")
