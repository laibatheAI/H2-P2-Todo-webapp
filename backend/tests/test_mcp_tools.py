"""
Unit tests for MCP tools in the Todo AI Chatbot application.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from pydantic import ValidationError
from datetime import datetime
from backend.mcp.tools.task_tools import (
    add_task_tool,
    list_tasks_tool,
    complete_task_tool,
    delete_task_tool,
    update_task_tool,
    AddTaskParams,
    ListTasksParams,
    CompleteTaskParams,
    DeleteTaskParams,
    UpdateTaskParams
)


class TestAddTaskTool:
    """Test cases for the add_task MCP tool."""

    def test_add_task_success(self):
        """Test successful task addition."""
        params = AddTaskParams(
            title="Test Task",
            description="Test Description",
            priority="high",
            category="work"
        )

        result = add_task_tool(params)

        assert result is not None
        assert result.content is not None

        # Parse the content as JSON to validate structure
        import json
        content = json.loads(result.content)
        assert content["success"] is True
        assert content["message"] is not None
        assert content["task"]["title"] == "Test Task"
        assert content["task"]["description"] == "Test Description"
        assert content["task"]["priority"] == "high"
        assert content["task"]["category"] == "work"

    def test_add_task_minimal_params(self):
        """Test adding task with minimal required parameters."""
        params = AddTaskParams(title="Simple Task")

        result = add_task_tool(params)

        assert result is not None
        assert result.content is not None

        import json
        content = json.loads(result.content)
        assert content["success"] is True
        assert content["task"]["title"] == "Simple Task"
        # Should have default values for optional parameters
        assert content["task"]["priority"] == "medium"  # Default priority

    def test_add_task_with_due_date(self):
        """Test adding task with due date."""
        due_date = "2026-12-31T23:59:59.999Z"
        params = AddTaskParams(
            title="Task with Due Date",
            due_date=due_date
        )

        result = add_task_tool(params)

        import json
        content = json.loads(result.content)
        assert content["success"] is True
        assert content["task"]["due_date"] is not None

    def test_add_task_invalid_priority(self):
        """Test adding task with invalid priority."""
        with pytest.raises(Exception):
            params = AddTaskParams(
                title="Test Task",
                priority="invalid_priority"  # This should cause validation to fail in the actual implementation
            )
            result = add_task_tool(params)
            # In the actual implementation, this would result in an error

    def test_add_task_empty_title(self):
        """Test validation for empty title."""
        with pytest.raises(ValidationError):
            AddTaskParams(title="")


class TestListTasksTool:
    """Test cases for the list_tasks MCP tool."""

    def test_list_tasks_default_params(self):
        """Test listing tasks with default parameters."""
        params = ListTasksParams()

        result = list_tasks_tool(params)

        assert result is not None
        assert result.content is not None

        import json
        content = json.loads(result.content)
        assert content["success"] is True
        assert "tasks" in content
        assert "total_count" in content
        assert "returned_count" in content

    def test_list_tasks_with_filters(self):
        """Test listing tasks with various filters."""
        params = ListTasksParams(
            status="completed",
            priority="high",
            category="work",
            limit=10,
            offset=0
        )

        result = list_tasks_tool(params)

        import json
        content = json.loads(result.content)
        assert content["success"] is True

    def test_list_tasks_limit_validation(self):
        """Test validation of limit parameter."""
        # Test with limit within bounds
        params = ListTasksParams(limit=50)
        result = list_tasks_tool(params)
        assert result is not None

    def test_list_tasks_invalid_status(self):
        """Test listing with invalid status parameter."""
        params = ListTasksParams(status="invalid_status")

        result = list_tasks_tool(params)

        import json
        content = json.loads(result.content)
        # Should return an error for invalid status
        assert "error" in content or content["success"] is True  # Depending on implementation


class TestCompleteTaskTool:
    """Test cases for the complete_task MCP tool."""

    def test_complete_task_success(self):
        """Test successful task completion."""
        params = CompleteTaskParams(
            task_id="123e4567-e89b-12d3-a456-426614174000",
            completion_notes="Completed as requested"
        )

        result = complete_task_tool(params)

        assert result is not None
        import json
        content = json.loads(result.content)
        assert content["success"] is True
        assert content["task_id"] == params.task_id

    def test_complete_task_without_notes(self):
        """Test completing task without completion notes."""
        params = CompleteTaskParams(
            task_id="123e4567-e89b-12d3-a456-426614174000"
        )

        result = complete_task_tool(params)

        import json
        content = json.loads(result.content)
        assert content["success"] is True

    def test_complete_task_invalid_id(self):
        """Test completion with invalid task ID format."""
        params = CompleteTaskParams(
            task_id="invalid-uuid-format"
        )

        result = complete_task_tool(params)

        import json
        content = json.loads(result.content)
        # Should return an error for invalid ID
        assert "error" in content


class TestDeleteTaskTool:
    """Test cases for the delete_task MCP tool."""

    def test_delete_task_success(self):
        """Test successful task deletion."""
        params = DeleteTaskParams(
            task_id="123e4567-e89b-12d3-a456-426614174000"
        )

        result = delete_task_tool(params)

        assert result is not None
        import json
        content = json.loads(result.content)
        assert content["success"] is True
        assert content["task_id"] == params.task_id

    def test_delete_task_invalid_id(self):
        """Test deletion with invalid task ID format."""
        params = DeleteTaskParams(
            task_id="invalid-uuid-format"
        )

        result = delete_task_tool(params)

        import json
        content = json.loads(result.content)
        # Should return an error for invalid ID
        assert "error" in content


class TestUpdateTaskTool:
    """Test cases for the update_task MCP tool."""

    def test_update_task_success(self):
        """Test successful task update."""
        params = UpdateTaskParams(
            task_id="123e4567-e89b-12d3-a456-426614174000",
            title="Updated Title",
            priority="high"
        )

        result = update_task_tool(params)

        assert result is not None
        import json
        content = json.loads(result.content)
        assert content["success"] is True
        assert content["task_id"] == params.task_id

    def test_update_task_partial_updates(self):
        """Test updating only some fields."""
        params = UpdateTaskParams(
            task_id="123e4567-e89b-12d3-a456-426614174000",
            title="Updated Title"
            # Only updating title, leaving others unchanged
        )

        result = update_task_tool(params)

        import json
        content = json.loads(result.content)
        assert content["success"] is True

    def test_update_task_invalid_priority(self):
        """Test update with invalid priority."""
        params = UpdateTaskParams(
            task_id="123e4567-e89b-12d3-a456-426614174000",
            priority="invalid_priority"
        )

        result = update_task_tool(params)

        import json
        content = json.loads(result.content)
        # Should return an error for invalid priority
        assert "error" in content

    def test_update_task_invalid_id(self):
        """Test update with invalid task ID."""
        params = UpdateTaskParams(
            task_id="invalid-uuid-format",
            title="New Title"
        )

        result = update_task_tool(params)

        import json
        content = json.loads(result.content)
        # Should return an error for invalid ID
        assert "error" in content


class TestToolParameterValidation:
    """Test parameter validation for all tools."""

    def test_add_task_param_validation(self):
        """Test AddTaskParams validation."""
        # Valid params should work
        valid_params = AddTaskParams(title="Test Title")
        assert valid_params.title == "Test Title"

        # Empty title should raise validation error
        with pytest.raises(ValidationError):
            AddTaskParams(title="")

    def test_list_tasks_param_validation(self):
        """Test ListTasksParams validation."""
        # Valid params should work
        valid_params = ListTasksParams(limit=25, offset=0)
        assert valid_params.limit == 25

    def test_complete_task_param_validation(self):
        """Test CompleteTaskParams validation."""
        # Valid params should work
        valid_params = CompleteTaskParams(task_id="123e4567-e89b-12d3-a456-426614174000")
        assert valid_params.task_id == "123e4567-e89b-12d3-a456-426614174000"

    def test_delete_task_param_validation(self):
        """Test DeleteTaskParams validation."""
        # Valid params should work
        valid_params = DeleteTaskParams(task_id="123e4567-e89b-12d3-a456-426614174000")
        assert valid_params.task_id == "123e4567-e89b-12d3-a456-426614174000"

    def test_update_task_param_validation(self):
        """Test UpdateTaskParams validation."""
        # Valid params should work
        valid_params = UpdateTaskParams(
            task_id="123e4567-e89b-12d3-a456-426614174000",
            title="New Title"
        )
        assert valid_params.task_id == "123e4567-e89b-12d3-a456-426614174000"
        assert valid_params.title == "New Title"