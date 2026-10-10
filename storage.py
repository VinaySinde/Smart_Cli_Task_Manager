
import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "tasks.json"


def load_tasks():
    """Load tasks from the JSON file."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            tasks = json.load(file)
            return tasks if isinstance(tasks, list) else []
    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read tasks.json. Starting with an empty list.")
        return []


def save_tasks(tasks):
    """Save tasks to the JSON file."""
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4, ensure_ascii=False)
    except OSError as error:
        print(f"Error saving tasks: {error}")
        raise
