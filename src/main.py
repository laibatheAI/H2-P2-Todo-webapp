from .storage import TaskManager
from .cli import display_menu, display_tasks, prompt_add_task, prompt_task_id, prompt_update_fields, confirm_delete
from .models import Task


def main():
    """
    Main application entry point and execution flow control.
    """
    print("Welcome to the Todo App!")
    task_manager = TaskManager()

    while True:
        display_menu()
        try:
            choice = input("Choose an option: ").strip()

            if choice == "1":
                # Add task
                try:
                    title, description = prompt_add_task()
                    task = task_manager.add_task(title, description)
                    print(f"Task added successfully with ID {task.id}")
                except ValueError as e:
                    print(f"Error: {e}")

            elif choice == "2":
                # View all tasks
                tasks = task_manager.list_tasks()
                display_tasks(tasks)

            elif choice == "3":
                # Update task
                try:
                    task_id = prompt_task_id()
                    task = task_manager.get_task(task_id)
                    print(f"Current task: {task.title}")

                    new_title, new_description = prompt_update_fields()
                    updated_task = task_manager.update_task(task_id, new_title, new_description)
                    print(f"Task {task_id} updated successfully")
                except ValueError as e:
                    print(f"Error: {e}")

            elif choice == "4":
                # Mark task as complete/incomplete
                try:
                    task_id = prompt_task_id()
                    task = task_manager.get_task(task_id)
                    updated_task = task_manager.toggle_complete(task_id)
                    status = "completed" if updated_task.completed else "incomplete"
                    print(f"Task {task_id} marked as {status}")
                except ValueError as e:
                    print(f"Error: {e}")

            elif choice == "5":
                # Delete task
                try:
                    task_id = prompt_task_id()
                    task = task_manager.get_task(task_id)
                    if confirm_delete(task):
                        task_manager.delete_task(task_id)
                        print(f"Task {task_id} deleted successfully")
                    else:
                        print("Deletion cancelled")
                except ValueError as e:
                    print(f"Error: {e}")

            elif choice == "6":
                # Exit
                print("Thank you for using the Todo App. Goodbye!")
                break

            else:
                print("Invalid option. Please choose a number between 1-6.")

        except KeyboardInterrupt:
            print("\n\nApplication interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()