from typing import List, Tuple, Optional
from .models import Task
import sys


def display_menu():
    """
    Display the main menu options to the user.
    """
    print("\n" + "="*16)
    print("Todo App Menu")
    print("="*16)
    print("1. Add task")
    print("2. View all tasks")
    print("3. Update task")
    print("4. Mark task as complete/incomplete")
    print("5. Delete task")
    print("6. Exit")
    print("="*16)


def display_tasks(tasks: List[Task]):
    """
    Format and display tasks in a table with status indicators.

    Args:
        tasks: List of Task objects to display
    """
    if not tasks:
        print("\nNo tasks yet. Add one to get started!")
        return

    # Print header
    print(f"\n{'ID':<4} {'Status':<8} {'Title':<25} {'Description':<35} {'Created':<17}")
    print("-" * 90)

    # Print each task
    for task in tasks:
        status = "[x]" if task.completed else "[ ]"
        title = task.title[:23] + ".." if len(task.title) > 23 else task.title
        description = task.description[:33] + ".." if len(task.description) > 33 else task.description
        created_str = task.created_at.strftime("%Y-%m-%d %H:%M")

        print(f"{task.id:<4} {status:<8} {title:<25} {description:<35} {created_str:<17}")


def prompt_add_task() -> Tuple[str, str]:
    """
    Prompt user for task title and description, return as tuple.

    Returns:
        Tuple containing (title, description)
    """
    title = input("Enter task title: ").strip()
    description = input("Enter task description (optional, press Enter to skip): ").strip()
    return title, description


def prompt_task_id() -> int:
    """
    Prompt user for task ID, validate and return integer.

    Returns:
        Valid task ID as integer

    Raises:
        ValueError: If input is not a valid positive integer
    """
    try:
        task_id_str = input("Enter task ID: ").strip()
        task_id = int(task_id_str)
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        return task_id
    except ValueError:
        if task_id_str.isdigit():
            raise ValueError("Task ID must be a positive integer")
        else:
            raise ValueError("Invalid input: Task ID must be a number")


def prompt_update_fields() -> Tuple[Optional[str], Optional[str]]:
    """
    Prompt user for new title/description, return as tuple (can be None).

    Returns:
        Tuple containing (new_title | None, new_description | None)
    """
    new_title_input = input("Enter new title (or press Enter to keep current): ").strip()
    new_title = new_title_input if new_title_input else None

    new_description_input = input("Enter new description (or press Enter to keep current): ").strip()
    new_description = new_description_input if new_description_input else None

    return new_title, new_description


def confirm_delete(task: Task) -> bool:
    """
    Prompt user for confirmation before deleting task.

    Args:
        task: Task object to be deleted

    Returns:
        Boolean indicating whether user confirmed deletion
    """
    print(f"\nAre you sure you want to delete task '{task.title}'?")
    confirmation = input("Type 'yes' to confirm deletion: ").strip().lower()
    return confirmation == 'yes'