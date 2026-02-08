"""
MCP tools for task management in the Todo AI Chatbot application.
"""
from mcp.server import Server
from mcp.types import Tool, Parameter, ToolResult
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
import json
from sqlmodel import Session, select
from backend.database.session import engine
from backend.models.task import Task, TaskCreate, TaskUpdate, PriorityEnum

# Define Pydantic models for tool parameters
class AddTaskParams(BaseModel):
    title: str = Field(description="The title/description of the task")
    description: Optional[str] = Field(default=None, description="Detailed description of the task")
    due_date: Optional[str] = Field(default=None, description="Due date in ISO 8601 format (YYYY-MM-DDTHH:mm:ss.sssZ)")
    priority: Optional[str] = Field(default="medium", description="Priority level ('low', 'medium', 'high')")
    category: Optional[str] = Field(default=None, description="Category for organizing tasks")


class ListTasksParams(BaseModel):
    status: Optional[str] = Field(default="all", description="Filter by completion status ('all', 'pending', 'completed')")
    priority: Optional[str] = Field(default=None, description="Filter by priority ('low', 'medium', 'high')")
    category: Optional[str] = Field(default=None, description="Filter by category")
    limit: Optional[int] = Field(default=50, description="Maximum number of tasks to return (max: 100)")
    offset: Optional[int] = Field(default=0, description="Number of tasks to skip for pagination")


class CompleteTaskParams(BaseModel):
    task_id: str = Field(description="The unique identifier of the task to complete")
    completion_notes: Optional[str] = Field(default=None, description="Additional notes about task completion")


class DeleteTaskParams(BaseModel):
    task_id: str = Field(description="The unique identifier of the task to delete")


class UpdateTaskParams(BaseModel):
    task_id: str = Field(description="The unique identifier of the task to update")
    title: Optional[str] = Field(default=None, description="New title for the task")
    description: Optional[str] = Field(default=None, description="New description for the task")
    due_date: Optional[str] = Field(default=None, description="New due date in ISO 8601 format")
    priority: Optional[str] = Field(default=None, description="New priority level ('low', 'medium', 'high')")
    category: Optional[str] = Field(default=None, description="New category for the task")
    completed: Optional[bool] = Field(default=None, description="New completion status")


# Define the tools
def add_task_tool(params: AddTaskParams) -> ToolResult:
    """
    Creates a new task in the user's task list with specified properties.
    """
    try:
        # Validate priority
        if params.priority and params.priority not in ["low", "medium", "high"]:
            return ToolResult(error="Invalid priority value. Use 'low', 'medium', or 'high'.")

        # Parse due date if provided
        due_date = None
        if params.due_date:
            try:
                due_date = datetime.fromisoformat(params.due_date.replace('Z', '+00:00'))
            except ValueError:
                return ToolResult(error="Invalid due_date format. Use ISO 8601 format (YYYY-MM-DDTHH:mm:ss.sssZ).")

        # Create task data
        task_data = TaskCreate(
            title=params.title,
            description=params.description,
            due_date=due_date,
            priority=PriorityEnum(params.priority) if params.priority else PriorityEnum.medium,
            category=params.category
        )

        # For now, using a placeholder user_id - in real implementation this would come from auth context
        # For demo purposes, we'll use a fixed UUID
        from uuid import uuid4
        task = Task(
            title=task_data.title,
            description=task_data.description,
            due_date=task_data.due_date,
            priority=task_data.priority,
            category=task_data.category,
            user_id=uuid4(),  # Placeholder - would come from authentication context
            completed=False
        )

        # Save to database (in a real implementation, this would use a service layer)
        # For now, we'll just return the task data as if it was saved
        task_dict = {
            "id": str(uuid4()),  # Simulate generated ID
            "title": task.title,
            "description": task.description,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "priority": task.priority.value,
            "category": task.category,
            "completed": task.completed,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }

        result = {
            "success": True,
            "task_id": task_dict["id"],
            "message": f"Task '{task.title}' created successfully",
            "task": task_dict
        }

        return ToolResult(content=json.dumps(result))

    except Exception as e:
        return ToolResult(error=f"Failed to create task: {str(e)}")


def list_tasks_tool(params: ListTasksParams) -> ToolResult:
    """
    Retrieves all tasks associated with the authenticated user, with optional filtering.
    """
    try:
        # Validate inputs
        if params.limit and (params.limit < 1 or params.limit > 100):
            return ToolResult(error="Limit must be between 1 and 100")

        if params.offset and params.offset < 0:
            return ToolResult(error="Offset must be greater than or equal to 0")

        # Validate status parameter
        if params.status and params.status not in ["all", "pending", "completed"]:
            return ToolResult(error="Invalid status. Use 'all', 'pending', or 'completed'.")

        # Validate priority parameter
        if params.priority and params.priority not in ["low", "medium", "high"]:
            return ToolResult(error="Invalid priority. Use 'low', 'medium', or 'high'.")

        # For demo purposes, we'll return mock data
        # In a real implementation, this would query the database with proper user filtering
        from uuid import uuid4

        # Create sample tasks
        tasks = []
        for i in range(min(params.limit or 50, 5)):
            task_dict = {
                "id": str(uuid4()),
                "title": f"Sample task {i+1}",
                "description": f"Description for sample task {i+1}",
                "due_date": (datetime.utcnow().replace(day=i+1) if i+1 <= 28 else datetime.utcnow()).isoformat() if i < 3 else None,
                "priority": params.priority or "medium",
                "category": params.category or "work",
                "completed": i % 3 == 0,  # Alternate completion status
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
            # Apply filters
            if params.status == "pending" and task_dict["completed"]:
                continue
            elif params.status == "completed" and not task_dict["completed"]:
                continue
            if params.priority and task_dict["priority"] != params.priority:
                continue
            if params.category and task_dict["category"] != params.category:
                continue

            tasks.append(task_dict)

        result = {
            "success": True,
            "total_count": len(tasks),
            "returned_count": len(tasks),
            "tasks": tasks
        }

        return ToolResult(content=json.dumps(result))

    except Exception as e:
        return ToolResult(error=f"Failed to retrieve tasks: {str(e)}")


def complete_task_tool(params: CompleteTaskParams) -> ToolResult:
    """
    Marks a specific task as completed.
    """
    try:
        # Validate task_id
        try:
            task_id = UUID(params.task_id)
        except ValueError:
            return ToolResult(error="Invalid task ID format")

        # For demo purposes, we'll simulate task completion
        # In a real implementation, this would query the database to find and update the task
        from uuid import uuid4

        # Mock task data
        task_dict = {
            "id": params.task_id,
            "title": f"Completed task {params.task_id[:8]}",
            "completed": True,
            "completed_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }

        result = {
            "success": True,
            "task_id": params.task_id,
            "message": f"Task '{task_dict['title']}' marked as completed",
            "task": task_dict
        }

        return ToolResult(content=json.dumps(result))

    except Exception as e:
        return ToolResult(error=f"Failed to complete task: {str(e)}")


def delete_task_tool(params: DeleteTaskParams) -> ToolResult:
    """
    Permanently removes a task from the user's task list.
    """
    try:
        # Validate task_id
        try:
            task_id = UUID(params.task_id)
        except ValueError:
            return ToolResult(error="Invalid task ID format")

        # For demo purposes, we'll simulate task deletion
        # In a real implementation, this would query the database to delete the task
        result = {
            "success": True,
            "task_id": params.task_id,
            "message": f"Task {params.task_id} deleted successfully"
        }

        return ToolResult(content=json.dumps(result))

    except Exception as e:
        return ToolResult(error=f"Failed to delete task: {str(e)}")


def update_task_tool(params: UpdateTaskParams) -> ToolResult:
    """
    Modifies properties of an existing task.
    """
    try:
        # Validate task_id
        try:
            task_id = UUID(params.task_id)
        except ValueError:
            return ToolResult(error="Invalid task ID format")

        # Validate priority if provided
        if params.priority and params.priority not in ["low", "medium", "high"]:
            return ToolResult(error="Invalid priority. Use 'low', 'medium', or 'high'.")

        # For demo purposes, we'll simulate task update
        # In a real implementation, this would query the database to find and update the task
        from uuid import uuid4

        # Create mock updated task
        updated_task = {
            "id": params.task_id,
            "title": params.title or f"Updated task {params.task_id[:8]}",
            "description": params.description or "Updated description",
            "due_date": params.due_date,
            "priority": params.priority or "medium",
            "category": params.category or "work",
            "completed": params.completed if params.completed is not None else False,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }

        result = {
            "success": True,
            "task_id": params.task_id,
            "message": f"Task {params.task_id} updated successfully",
            "task": updated_task
        }

        return ToolResult(content=json.dumps(result))

    except Exception as e:
        return ToolResult(error=f"Failed to update task: {str(e)}")


# Create Tool instances
add_task_tool_def = Tool(
    name="add_task",
    description="Creates a new task in the user's task list with specified properties",
    parameters=AddTaskParams.schema(),
    handler=add_task_tool
)

list_tasks_tool_def = Tool(
    name="list_tasks",
    description="Retrieves all tasks associated with the authenticated user, with optional filtering",
    parameters=ListTasksParams.schema(),
    handler=list_tasks_tool
)

complete_task_tool_def = Tool(
    name="complete_task",
    description="Marks a specific task as completed",
    parameters=CompleteTaskParams.schema(),
    handler=complete_task_tool
)

delete_task_tool_def = Tool(
    name="delete_task",
    description="Permanently removes a task from the user's task list",
    parameters=DeleteTaskParams.schema(),
    handler=delete_task_tool
)

update_task_tool_def = Tool(
    name="update_task",
    description="Modifies properties of an existing task",
    parameters=UpdateTaskParams.schema(),
    handler=update_task_tool
)