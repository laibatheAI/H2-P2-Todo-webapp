"""
Conversation service for the Todo AI Chatbot application.
Handles the core logic for managing conversations and orchestrating agent interactions.
"""
from typing import Dict, Any, List, Optional
import asyncio
from datetime import datetime
import uuid

from backend.core.agents.todo_agent import TodoAgent
from backend.core.agents.tool_wiring import route_and_execute_tool
from backend.models.conversation import Conversation
from backend.models.message import Message, MessageRoleEnum
from backend.database.session import get_session
from sqlmodel import Session, select
from backend.config import settings


class ChatService:
    """
    Service class for handling chat-related operations and conversation management.
    """

    def __init__(self, agent: TodoAgent):
        self.agent = agent

    async def process_message(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        user_id: str
    ) -> Dict[str, Any]:
        """
        Process a user message through the AI agent and return the response.

        Args:
            user_message: The message from the user
            conversation_history: History of previous messages in the conversation
            user_id: The ID of the authenticated user

        Returns:
            Dictionary containing the agent's response and any tool calls
        """
        try:
            # Process the message through the agent
            response = await self.agent.process_message(
                user_message=user_message,
                conversation_history=conversation_history,
                user_id=user_id
            )

            return response

        except Exception as e:
            return {
                "content": f"I'm sorry, I encountered an error processing your request: {str(e)}",
                "role": "assistant",
                "error": str(e)
            }

    async def create_conversation(self, user_id: str, title: Optional[str] = None) -> Conversation:
        """
        Create a new conversation for the user.

        Args:
            user_id: The ID of the user creating the conversation
            title: Optional title for the conversation

        Returns:
            Created Conversation object
        """
        # In a real implementation, we would create this in the database
        # For now, we'll simulate the creation
        conversation = Conversation(
            id=uuid.uuid4(),
            user_id=uuid.UUID(user_id),
            title=title,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            last_accessed_at=datetime.utcnow()
        )

        return conversation

    async def get_or_create_conversation(self, user_id: str, conversation_id: Optional[str] = None) -> Conversation:
        """
        Get an existing conversation or create a new one if none exists.

        Args:
            user_id: The ID of the user
            conversation_id: Optional existing conversation ID

        Returns:
            Conversation object
        """
        # If no conversation ID provided, create a new one
        if not conversation_id:
            return await self.create_conversation(user_id)

        # In a real implementation, we would fetch from the database
        # For simulation, we'll create a conversation with the provided ID
        conversation = Conversation(
            id=uuid.UUID(conversation_id),
            user_id=uuid.UUID(user_id),
            title=f"Conversation {conversation_id[:8]}",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            last_accessed_at=datetime.utcnow()
        )

        return conversation

    async def update_conversation_title(self, conversation_id: str, title: str, user_id: str) -> bool:
        """
        Update the title of a conversation.

        Args:
            conversation_id: The ID of the conversation to update
            title: The new title for the conversation
            user_id: The ID of the user who owns the conversation

        Returns:
            True if update was successful, False otherwise
        """
        # In a real implementation, this would update the database
        # For simulation, we'll return True
        return True

    async def get_conversation_stats(self, user_id: str) -> Dict[str, Any]:
        """
        Get statistics about the user's conversations.

        Args:
            user_id: The ID of the user

        Returns:
            Dictionary containing conversation statistics
        """
        # In a real implementation, this would query the database
        # For simulation, we'll return mock stats
        return {
            "total_conversations": 5,
            "active_conversations": 2,
            "total_messages": 42,
            "average_messages_per_conversation": 8.4,
            "last_activity": datetime.utcnow().isoformat()
        }

    async def handle_tool_execution(self, tool_calls: List[Dict[str, Any]], user_id: str) -> List[Dict[str, Any]]:
        """
        Handle the execution of tools requested by the agent.

        Args:
            tool_calls: List of tool calls requested by the agent
            user_id: The ID of the authenticated user

        Returns:
            List of tool execution results
        """
        results = []

        for tool_call in tool_calls:
            # Extract function name and arguments
            function_name = tool_call.get("function", {}).get("name")
            function_args = tool_call.get("function", {}).get("arguments", {})

            if isinstance(function_args, str):
                import json
                try:
                    function_args = json.loads(function_args)
                except json.JSONDecodeError:
                    results.append({
                        "tool_call_id": tool_call.get("id"),
                        "result": {"success": False, "error": "Invalid function arguments format"}
                    })
                    continue

            # Add user context to function arguments
            function_args["user_id"] = user_id

            try:
                # Execute the tool based on its name
                if function_name == "add_task":
                    # In a real implementation, this would call the MCP tool directly
                    result = await self.execute_add_task(function_args)
                elif function_name == "list_tasks":
                    result = await self.execute_list_tasks(function_args)
                elif function_name == "complete_task":
                    result = await self.execute_complete_task(function_args)
                elif function_name == "delete_task":
                    result = await self.execute_delete_task(function_args)
                elif function_name == "update_task":
                    result = await self.execute_update_task(function_args)
                else:
                    result = {"success": False, "error": f"Unknown tool: {function_name}"}

                results.append({
                    "tool_call_id": tool_call.get("id"),
                    "result": result
                })

            except Exception as e:
                results.append({
                    "tool_call_id": tool_call.get("id"),
                    "result": {"success": False, "error": str(e)}
                })

        return results

    async def execute_add_task(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the add_task tool."""
        # This would normally call the MCP add_task tool
        # For simulation, we'll return a mock response
        from backend.models.task import PriorityEnum

        priority = args.get('priority', 'medium')
        if priority not in ['low', 'medium', 'high']:
            priority = 'medium'

        mock_task = {
            "id": str(uuid.uuid4()),
            "title": args.get('title', 'Untitled Task'),
            "description": args.get('description'),
            "due_date": args.get('due_date'),
            "priority": priority,
            "category": args.get('category'),
            "completed": False,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }

        return {
            "success": True,
            "task_id": mock_task["id"],
            "message": f"Task '{mock_task['title']}' added successfully",
            "task": mock_task
        }

    async def execute_list_tasks(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the list_tasks tool."""
        # This would normally call the MCP list_tasks tool
        # For simulation, we'll return mock tasks
        mock_tasks = [
            {
                "id": str(uuid.uuid4()),
                "title": "Sample task 1",
                "description": "This is a sample task",
                "due_date": "2026-02-10T10:00:00.000Z",
                "priority": "medium",
                "category": "work",
                "completed": False,
                "created_at": "2026-02-01T10:00:00.000Z",
                "updated_at": "2026-02-01T10:00:00.000Z"
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Sample task 2",
                "description": "Another sample task",
                "due_date": "2026-02-15T14:00:00.000Z",
                "priority": "high",
                "category": "personal",
                "completed": True,
                "created_at": "2026-02-02T10:00:00.000Z",
                "updated_at": "2026-02-03T10:00:00.000Z"
            }
        ]

        # Apply filters if provided
        status_filter = args.get('status', 'all')
        if status_filter == 'completed':
            mock_tasks = [t for t in mock_tasks if t['completed']]
        elif status_filter == 'pending':
            mock_tasks = [t for t in mock_tasks if not t['completed']]

        priority_filter = args.get('priority')
        if priority_filter:
            mock_tasks = [t for t in mock_tasks if t['priority'] == priority_filter]

        category_filter = args.get('category')
        if category_filter:
            mock_tasks = [t for t in mock_tasks if t['category'] == category_filter]

        limit = args.get('limit', 50)
        mock_tasks = mock_tasks[:limit]

        return {
            "success": True,
            "total_count": len(mock_tasks),
            "returned_count": len(mock_tasks),
            "tasks": mock_tasks
        }

    async def execute_complete_task(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the complete_task tool."""
        # This would normally call the MCP complete_task tool
        # For simulation, we'll return a mock response
        task_id = args.get('task_id')
        if not task_id:
            return {
                "success": False,
                "error": "task_id is required"
            }

        return {
            "success": True,
            "task_id": task_id,
            "message": f"Task {task_id} marked as completed",
            "completion_notes": args.get('completion_notes')
        }

    async def execute_delete_task(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the delete_task tool."""
        # This would normally call the MCP delete_task tool
        # For simulation, we'll return a mock response
        task_id = args.get('task_id')
        if not task_id:
            return {
                "success": False,
                "error": "task_id is required"
            }

        return {
            "success": True,
            "task_id": task_id,
            "message": f"Task {task_id} deleted successfully"
        }

    async def execute_update_task(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the update_task tool."""
        # This would normally call the MCP update_task tool
        # For simulation, we'll return a mock response
        task_id = args.get('task_id')
        if not task_id:
            return {
                "success": False,
                "error": "task_id is required"
            }

        return {
            "success": True,
            "task_id": task_id,
            "message": f"Task {task_id} updated successfully"
        }

    async def cleanup_old_conversations(self, days_to_retain: int = 90) -> int:
        """
        Clean up conversations older than the specified number of days.

        Args:
            days_to_retain: Number of days to retain conversations

        Returns:
            Number of conversations deleted
        """
        # In a real implementation, this would delete old conversations from the database
        # For simulation, we'll return 0
        return 0