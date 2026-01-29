# API Contracts: Todo In-Memory Python Console App

## TaskManager Class Contract

### Methods

#### add_task(title: str, description: str = "") -> Task
- **Purpose**: Add a new task to the collection
- **Parameters**:
  - title (str): Required task title, must be non-empty after stripping whitespace
  - description (str): Optional task description, defaults to empty string
- **Returns**: Task object with assigned ID and creation timestamp
- **Exceptions**: ValueError if title is empty after stripping
- **Side effects**: Increments internal ID counter, adds task to collection

#### list_tasks() -> list[Task]
- **Purpose**: Retrieve all tasks in the collection
- **Parameters**: None
- **Returns**: List of all Task objects, sorted by creation order (oldest first)
- **Exceptions**: None
- **Side effects**: None

#### get_task(task_id: int) -> Task
- **Purpose**: Retrieve a specific task by ID
- **Parameters**:
  - task_id (int): Positive integer ID of the task to retrieve
- **Returns**: Task object matching the ID
- **Exceptions**: ValueError if task with given ID does not exist
- **Side effects**: None

#### update_task(task_id: int, title: str | None = None, description: str | None = None) -> Task
- **Purpose**: Update specific fields of an existing task
- **Parameters**:
  - task_id (int): Positive integer ID of the task to update
  - title (str | None): Optional new title, if None then field is unchanged
  - description (str | None): Optional new description, if None then field is unchanged
- **Returns**: Updated Task object
- **Exceptions**:
  - ValueError if task with given ID does not exist
  - ValueError if title is provided but is empty after stripping
- **Side effects**: Modifies the specified task in the collection

#### toggle_complete(task_id: int) -> Task
- **Purpose**: Toggle the completion status of a task
- **Parameters**:
  - task_id (int): Positive integer ID of the task to update
- **Returns**: Updated Task object with toggled completion status
- **Exceptions**: ValueError if task with given ID does not exist
- **Side effects**: Changes the completed status of the specified task

#### delete_task(task_id: int) -> None
- **Purpose**: Remove a task from the collection
- **Parameters**:
  - task_id (int): Positive integer ID of the task to delete
- **Returns**: None
- **Exceptions**: ValueError if task with given ID does not exist
- **Side effects**: Removes the specified task from the collection

## CLI Interface Contract

### Functions

#### display_menu()
- **Purpose**: Display the main menu options to the user
- **Parameters**: None
- **Returns**: None
- **Side effects**: Prints menu to console

#### display_tasks(tasks: list[Task])
- **Purpose**: Format and display tasks in a table with status indicators
- **Parameters**:
  - tasks (list[Task]): List of Task objects to display
- **Returns**: None
- **Side effects**: Prints formatted task list to console

#### prompt_add_task() -> tuple[str, str]
- **Purpose**: Prompt user for task title and description
- **Parameters**: None
- **Returns**: Tuple containing (title, description)
- **Side effects**: Interacts with user via console input

#### prompt_task_id() -> int
- **Purpose**: Prompt user for task ID, validate and return integer
- **Parameters**: None
- **Returns**: Valid task ID as integer
- **Exceptions**: ValueError if input is not a valid positive integer
- **Side effects**: Interacts with user via console input

#### prompt_update_fields() -> tuple[str | None, str | None]
- **Purpose**: Prompt user for new title/description, return as tuple (can be None)
- **Parameters**: None
- **Returns**: Tuple containing (new_title | None, new_description | None)
- **Side effects**: Interacts with user via console input

#### confirm_delete(task: Task) -> bool
- **Purpose**: Prompt user for confirmation before deleting task
- **Parameters**:
  - task (Task): Task object to be deleted
- **Returns**: Boolean indicating whether user confirmed deletion
- **Side effects**: Interacts with user via console input