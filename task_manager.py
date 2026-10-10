
from storage import load_tasks, save_tasks
from utils import get_due_date, get_priority, get_task_status, print_task


class TaskManager:
    def __init__(self):
        self.tasks = load_tasks()

    def _next_id(self):
        """Generate a unique ID."""
        return max((task["id"] for task in self.tasks), default=0) + 1

    def add_task(self):
        title = input("Task title: ").strip()

        if not title:
            print("Task title cannot be empty.")
            return

        description = input("Description (optional): ").strip()
        priority = get_priority()
        due_date = get_due_date()

        task = {
            "id": self._next_id(),
            "title": title,
            "description": description,
            "priority": priority,
            "due_date": due_date,
            "completed": False
        }

        self.tasks.append(task)
        save_tasks(self.tasks)
        print(f"Task added successfully. ID: {task['id']}")

    def view_tasks(self, tasks=None):
        tasks = self.tasks if tasks is None else tasks

        if not tasks:
            print("No tasks found.")
            return

        priority_order = {"high": 0, "medium": 1, "low": 2}
        sorted_tasks = sorted(
            tasks,
            key=lambda task: (
                task["completed"],
                priority_order.get(task["priority"], 3),
                task.get("due_date") or "9999-12-31"
            )
        )

        for task in sorted_tasks:
            print_task(task)

        print("-" * 60)

    def _find_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None

    def _ask_task_id(self):
        try:
            task_id = int(input("Enter task ID: ").strip())
            return task_id if task_id > 0 else None
        except ValueError:
            print("Please enter a valid numeric ID.")
            return None

    def update_task(self):
        task_id = self._ask_task_id()
        task = self._find_task(task_id) if task_id else None

        if not task:
            print("Task not found.")
            return

        print("Press Enter to keep the existing value.")

        title = input(f"Title [{task['title']}]: ").strip()
        if title:
            task["title"] = title

        description = input(
            f"Description [{task.get('description', '')}]: "
        ).strip()
        if description:
            task["description"] = description

        priority = input(
            f"Priority [{task['priority']}] (high/medium/low): "
        ).strip().lower()

        if priority:
            if priority not in ("high", "medium", "low"):
                print("Invalid priority. Task was not updated.")
                return
            task["priority"] = priority

        due_date = input(
            f"Due date [{task.get('due_date') or 'None'}] "
            "(YYYY-MM-DD, none, or Enter to keep): "
        ).strip()

        if due_date.lower() == "none":
            task["due_date"] = None
        elif due_date:
            from datetime import date

            try:
                date.fromisoformat(due_date)
                task["due_date"] = due_date
            except ValueError:
                print("Invalid date. Task was not updated.")
                return

        save_tasks(self.tasks)
        print("Task updated successfully.")

    def delete_task(self):
        task_id = self._ask_task_id()
        task = self._find_task(task_id) if task_id else None

        if not task:
            print("Task not found.")
            return

        confirm = input(
            f"Delete '{task['title']}'? (y/n): "
        ).strip().lower()

        if confirm == "y":
            self.tasks.remove(task)
            save_tasks(self.tasks)
            print("Task deleted successfully.")
        else:
            print("Deletion cancelled.")

    def complete_task(self):
        task_id = self._ask_task_id()
        task = self._find_task(task_id) if task_id else None

        if not task:
            print("Task not found.")
            return

        if task["completed"]:
            print("This task is already completed.")
            return

        task["completed"] = True
        save_tasks(self.tasks)
        print("Task marked as completed.")

    def search_tasks(self):
        keyword = input("Search title or description: ").strip().lower()

        if not keyword:
            print("Please enter a search term.")
            return

        results = [
            task for task in self.tasks
            if keyword in task["title"].lower()
            or keyword in task.get("description", "").lower()
        ]

        self.view_tasks(results)

    def view_overdue_tasks(self):
        overdue = [
            task for task in self.tasks
            if get_task_status(task) == "OVERDUE"
        ]
        print("\nOVERDUE TASKS")
        self.view_tasks(overdue)

    def filter_tasks(self):
        print("1. Pending")
        print("2. Completed")
        print("3. High priority")
        print("4. Medium priority")
        print("5. Low priority")

        choice = input("Choose filter: ").strip()

        filters = {
            "1": lambda task: not task["completed"],
            "2": lambda task: task["completed"],
            "3": lambda task: task["priority"] == "high",
            "4": lambda task: task["priority"] == "medium",
            "5": lambda task: task["priority"] == "low"
        }

        if choice not in filters:
            print("Invalid filter.")
            return

        self.view_tasks([
            task for task in self.tasks if filters[choice](task)
        ])

    def statistics(self):
        total = len(self.tasks)
        completed = sum(task["completed"] for task in self.tasks)
        pending = total - completed
        overdue = sum(
            get_task_status(task) == "OVERDUE"
            for task in self.tasks
        )

        completion_rate = (
            completed / total * 100 if total else 0
        )

        print("\n========== TASK STATISTICS ==========")
        print(f"Total tasks      : {total}")
        print(f"Completed        : {completed}")
        print(f"Pending          : {pending}")
        print(f"Overdue          : {overdue}")
        print(f"Completion rate  : {completion_rate:.1f}%")
        print("=====================================")
