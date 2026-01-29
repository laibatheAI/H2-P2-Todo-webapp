# Quickstart Guide: Todo In-Memory Python Console App

## Prerequisites

- Python 3.13+ installed
- UV package manager installed

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Install dependencies (if any):
   ```bash
   uv sync  # or appropriate command for your project
   ```

## Running the Application

1. Execute the main application:
   ```bash
   python -m src.main
   ```

2. The application will display a main menu with numbered options:
   ```
   ================
   Todo App Menu
   ================
   1. Add task
   2. View all tasks
   3. Update task
   4. Mark task as complete/incomplete
   5. Delete task
   6. Exit
   ================
   Choose an option:
   ```

## Basic Usage

### Adding a Task
1. Select option 1
2. Enter the task title when prompted
3. Optionally enter a description when prompted
4. The task will be added with a confirmation message

### Viewing Tasks
1. Select option 2
2. The application will display all tasks in a formatted table:
   ```
   ID  Status  Title           Description      Created
   1   [ ]     Sample task     A description   2025-12-30 14:30
   2   [x]     Completed task                  2025-12-30 14:32
   ```

### Updating a Task
1. Select option 3
2. Enter the task ID when prompted
3. Optionally enter a new title (press Enter to skip)
4. Optionally enter a new description (press Enter to skip)
5. The task will be updated with a confirmation message

### Marking Task Complete/Incomplete
1. Select option 4
2. Enter the task ID when prompted
3. The task's completion status will be toggled with a confirmation message

### Deleting a Task
1. Select option 5
2. Enter the task ID when prompted
3. Confirm the deletion when prompted
4. The task will be deleted with a confirmation message

### Exiting the Application
1. Select option 6
2. The application will terminate gracefully

## Error Handling

- Invalid menu options will display an error message and return to the main menu
- Invalid task IDs will display a clear error message
- Empty or invalid input will display user-friendly error messages
- The application will never crash on invalid input

## Project Structure

```
src/
├── models.py      # Task dataclass definition
├── storage.py     # TaskManager class with CRUD operations
├── cli.py         # CLI interface functions
└── main.py        # Main application entry point
specs/             # Specification files
├── 001-todo-console-app/
│   ├── spec.md    # Feature specification
│   ├── plan.md    # Implementation plan
│   └── plan/      # Planning artifacts
└── ...
```