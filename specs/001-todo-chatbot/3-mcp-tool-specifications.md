# MCP Tool Specifications: Todo AI Chatbot

## Overview

This document defines the Model Context Protocol (MCP) tools available to the Todo AI Agent for performing task management operations. Each tool follows a stateless, database-backed architecture to ensure server statelessness.

## Tool: add_task

### Purpose
Creates a new task in the user's task list with specified properties.

### Input Parameters
- `title` (string, required): The title/description of the task
- `description` (string, optional): Detailed description of the task
- `due_date` (string, optional): Due date in ISO 8601 format (YYYY-MM-DDTHH:mm:ss.sssZ)
- `priority` (string, optional): Priority level ("low", "medium", "high", default: "medium")
- `category` (string, optional): Category for organizing tasks

### Database Interactions
- Creates a new record in the `tasks` table
- Associates the task with the authenticated user ID from JWT
- Sets `created_at` timestamp to current time
- Sets `completed` to false by default
- Generates a unique UUID for the task

### Output Schema
```json
{
  "success": boolean,
  "task_id": string,
  "message": string,
  "task": {
    "id": string,
    "title": string,
    "description": string,
    "due_date": string,
    "priority": string,
    "category": string,
    "completed": boolean,
    "created_at": string,
    "updated_at": string
  }
}
```

### Error Scenarios and Responses
- **Missing title**: Returns error with message "Task title is required"
- **Database constraint violation**: Returns error with message "Failed to create task due to invalid data"
- **Authentication failure**: Returns error with message "Unauthorized to create tasks"
- **Database connection error**: Returns error with message "Service temporarily unavailable"

## Tool: list_tasks

### Purpose
Retrieves all tasks associated with the authenticated user, with optional filtering.

### Input Parameters
- `status` (string, optional): Filter by completion status ("all", "pending", "completed", default: "all")
- `priority` (string, optional): Filter by priority ("low", "medium", "high")
- `category` (string, optional): Filter by category
- `limit` (integer, optional): Maximum number of tasks to return (default: 50, max: 100)
- `offset` (integer, optional): Number of tasks to skip for pagination (default: 0)

### Database Interactions
- Queries the `tasks` table filtered by user ID from JWT
- Applies filters based on input parameters
- Orders results by creation date (newest first) or due date if specified
- Returns paginated results according to limit/offset

### Output Schema
```json
{
  "success": boolean,
  "total_count": integer,
  "returned_count": integer,
  "tasks": [
    {
      "id": string,
      "title": string,
      "description": string,
      "due_date": string,
      "priority": string,
      "category": string,
      "completed": boolean,
      "created_at": string,
      "updated_at": string
    }
  ]
}
```

### Error Scenarios and Responses
- **Authentication failure**: Returns error with message "Unauthorized to view tasks"
- **Database connection error**: Returns error with message "Failed to retrieve tasks"
- **Invalid parameters**: Returns error with message "Invalid filter parameters provided"

## Tool: complete_task

### Purpose
Marks a specific task as completed.

### Input Parameters
- `task_id` (string, required): The unique identifier of the task to complete
- `completion_notes` (string, optional): Additional notes about task completion

### Database Interactions
- Finds the task by ID and user ID from JWT
- Updates the `completed` field to true
- Sets `completed_at` timestamp to current time
- Updates `updated_at` timestamp

### Output Schema
```json
{
  "success": boolean,
  "task_id": string,
  "message": string,
  "task": {
    "id": string,
    "title": string,
    "completed": boolean,
    "completed_at": string,
    "updated_at": string
  }
}
```

### Error Scenarios and Responses
- **Task not found**: Returns error with message "Task not found or does not belong to user"
- **Task already completed**: Returns error with message "Task is already marked as completed"
- **Authentication failure**: Returns error with message "Unauthorized to complete task"
- **Database connection error**: Returns error with message "Failed to update task"

## Tool: delete_task

### Purpose
Permanently removes a task from the user's task list.

### Input Parameters
- `task_id` (string, required): The unique identifier of the task to delete

### Database Interactions
- Verifies the task belongs to the authenticated user
- Deletes the task record from the `tasks` table
- Logs the deletion for audit purposes

### Output Schema
```json
{
  "success": boolean,
  "task_id": string,
  "message": string
}
```

### Error Scenarios and Responses
- **Task not found**: Returns error with message "Task not found or does not belong to user"
- **Authentication failure**: Returns error with message "Unauthorized to delete task"
- **Database connection error**: Returns error with message "Failed to delete task"

## Tool: update_task

### Purpose
Modifies properties of an existing task.

### Input Parameters
- `task_id` (string, required): The unique identifier of the task to update
- `title` (string, optional): New title for the task
- `description` (string, optional): New description for the task
- `due_date` (string, optional): New due date in ISO 8601 format
- `priority` (string, optional): New priority level ("low", "medium", "high")
- `category` (string, optional): New category for the task
- `completed` (boolean, optional): New completion status

### Database Interactions
- Finds the task by ID and user ID from JWT
- Updates only the fields provided in the input
- Updates the `updated_at` timestamp
- Validates that the user owns the task

### Output Schema
```json
{
  "success": boolean,
  "task_id": string,
  "message": string,
  "task": {
    "id": string,
    "title": string,
    "description": string,
    "due_date": string,
    "priority": string,
    "category": string,
    "completed": boolean,
    "created_at": string,
    "updated_at": string
  }
}
```

### Error Scenarios and Responses
- **Task not found**: Returns error with message "Task not found or does not belong to user"
- **No update parameters**: Returns error with message "No fields provided to update"
- **Authentication failure**: Returns error with message "Unauthorized to update task"
- **Database connection error**: Returns error with message "Failed to update task"
- **Invalid field values**: Returns error with specific validation messages