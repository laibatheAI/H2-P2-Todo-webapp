"""
Main agent implementation for the Todo AI Chatbot application.
"""
import asyncio
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

from backend.config import settings
from backend.mcp.server import server

# Handle OpenAI import with graceful fallback
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    # Define a mock OpenAI client for graceful degradation
    class MockOpenAIClient:
        def __init__(self, api_key=None):
            pass
            
        def chat(self):
            pass
            
        class completions:
            @staticmethod
            def create(*args, **kwargs):
                # Return a mock response
                class MockChoice:
                    def __init__(self):
                        class MockMessage:
                            def __init__(self):
                                self.content = "Mock response: AI agent is not available"
                                self.tool_calls = None
                        
                        self.message = MockMessage()
                
                class MockResponse:
                    def __init__(self):
                        self.choices = [MockChoice()]
                
                return MockResponse()
    
    class OpenAI:
        def __init__(self, api_key=None):
            pass
            
        def chat(self):
            return MockOpenAIClient()
            
        class completions:
            @staticmethod
            def create(*args, **kwargs):
                return MockOpenAIClient.completions.create()
    
    OPENAI_AVAILABLE = False


class AgentConfig(BaseModel):
    """Configuration for the Todo AI Agent."""
    model: str = "gpt-4-turbo-preview"
    temperature: float = 0.7
    max_tokens: int = 1000
    system_prompt: str = (
        "You are a helpful and efficient Todo AI Assistant. "
        "Your role is to help users manage their tasks through natural language conversations. "
        "You have access to tools that allow you to create, list, update, complete, and delete tasks."
    )


class TodoAgent:
    """Main agent class for handling todo management conversations."""

    def __init__(self, config: Optional[AgentConfig] = None):
        self.config = config or AgentConfig()
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def get_system_prompt(self) -> str:
        """Return the system prompt for the agent."""
        return self.config.system_prompt

    async def process_message(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        user_id: str
    ) -> Dict[str, Any]:
        """
        Process a user message and return an appropriate response.

        Args:
            user_message: The message from the user
            conversation_history: History of previous messages
            user_id: The ID of the authenticated user

        Returns:
            Dictionary containing the agent's response and any tool calls
        """
        # Prepare messages for the OpenAI API
        messages = [{"role": "system", "content": self.get_system_prompt()}]

        # Add conversation history
        for msg in conversation_history:
            messages.append({"role": msg["role"], "content": msg["content"]})

        # Add the current user message
        messages.append({"role": "user", "content": user_message})

        try:
            # Call the OpenAI API with tool support
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                tools=self._get_available_tools(),
                tool_choice="auto",
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature
            )

            # Extract the response
            choice = response.choices[0]
            message = choice.message

            result = {
                "content": message.content or "",
                "role": "assistant",
                "tool_calls": [],
                "tool_results": []
            }

            # Process any tool calls
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    # Execute the tool and capture results
                    tool_result = await self._execute_tool_call(tool_call, user_id)
                    result["tool_calls"].append({
                        "id": tool_call.id,
                        "type": tool_call.type,
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments
                        }
                    })
                    result["tool_results"].append({
                        "tool_call_id": tool_call.id,
                        "result": tool_result
                    })

            return result

        except Exception as e:
            return {
                "content": f"I'm sorry, I encountered an error processing your request: {str(e)}",
                "role": "assistant",
                "error": str(e)
            }

    def _get_available_tools(self) -> List[Dict[str, Any]]:
        """
        Return the list of available tools that the agent can use.
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Creates a new task in the user's task list with specified properties",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "The title/description of the task"},
                            "description": {"type": "string", "description": "Detailed description of the task"},
                            "due_date": {"type": "string", "description": "Due date in ISO 8601 format (YYYY-MM-DDTHH:mm:ss.sssZ)"},
                            "priority": {"type": "string", "description": "Priority level ('low', 'medium', 'high')", "enum": ["low", "medium", "high"]},
                            "category": {"type": "string", "description": "Category for organizing tasks"}
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "Retrieves all tasks associated with the authenticated user, with optional filtering",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string", "description": "Filter by completion status ('all', 'pending', 'completed')", "enum": ["all", "pending", "completed"]},
                            "priority": {"type": "string", "description": "Filter by priority ('low', 'medium', 'high')", "enum": ["low", "medium", "high"]},
                            "category": {"type": "string", "description": "Filter by category"},
                            "limit": {"type": "integer", "description": "Maximum number of tasks to return (max: 100)"},
                            "offset": {"type": "integer", "description": "Number of tasks to skip for pagination"}
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Marks a specific task as completed",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string", "description": "The unique identifier of the task to complete"},
                            "completion_notes": {"type": "string", "description": "Additional notes about task completion"}
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Permanently removes a task from the user's task list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string", "description": "The unique identifier of the task to delete"}
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Modifies properties of an existing task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string", "description": "The unique identifier of the task to update"},
                            "title": {"type": "string", "description": "New title for the task"},
                            "description": {"type": "string", "description": "New description for the task"},
                            "due_date": {"type": "string", "description": "New due date in ISO 8601 format"},
                            "priority": {"type": "string", "description": "New priority level ('low', 'medium', 'high')", "enum": ["low", "medium", "high"]},
                            "category": {"type": "string", "description": "New category for the task"},
                            "completed": {"type": "boolean", "description": "New completion status"}
                        },
                        "required": ["task_id"]
                    }
                }
            }
        ]

    async def _execute_tool_call(self, tool_call, user_id: str) -> Dict[str, Any]:
        """
        Execute a tool call and return the result.

        Args:
            tool_call: The tool call to execute
            user_id: The ID of the authenticated user

        Returns:
            Result of the tool execution
        """
        # In a real implementation, this would make actual calls to the MCP tools
        # For now, we'll simulate tool execution

        import json
        from uuid import uuid4

        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)

        # Add user context to function args
        function_args['user_id'] = user_id

        try:
            # Simulate different tool responses based on the function called
            if function_name == "add_task":
                return {
                    "success": True,
                    "task_id": str(uuid4()),
                    "message": f"Task '{function_args.get('title', 'Untitled')}' added successfully",
                    "task": {
                        "id": str(uuid4()),
                        "title": function_args.get('title'),
                        "description": function_args.get('description'),
                        "due_date": function_args.get('due_date'),
                        "priority": function_args.get('priority', 'medium'),
                        "category": function_args.get('category'),
                        "completed": False,
                        "created_at": "2026-02-05T12:00:00.000Z",
                        "updated_at": "2026-02-05T12:00:00.000Z"
                    }
                }
            elif function_name == "list_tasks":
                # Create mock task list
                mock_tasks = [
                    {
                        "id": str(uuid4()),
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
                        "id": str(uuid4()),
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
                status = function_args.get('status')
                if status == 'completed':
                    mock_tasks = [t for t in mock_tasks if t['completed']]
                elif status == 'pending':
                    mock_tasks = [t for t in mock_tasks if not t['completed']]

                priority = function_args.get('priority')
                if priority:
                    mock_tasks = [t for t in mock_tasks if t['priority'] == priority]

                category = function_args.get('category')
                if category:
                    mock_tasks = [t for t in mock_tasks if t['category'] == category]

                limit = function_args.get('limit', 50)
                mock_tasks = mock_tasks[:limit]

                return {
                    "success": True,
                    "total_count": len(mock_tasks),
                    "returned_count": len(mock_tasks),
                    "tasks": mock_tasks
                }
            elif function_name == "complete_task":
                return {
                    "success": True,
                    "task_id": function_args.get('task_id'),
                    "message": f"Task {function_args.get('task_id')} marked as completed"
                }
            elif function_name == "delete_task":
                return {
                    "success": True,
                    "task_id": function_args.get('task_id'),
                    "message": f"Task {function_args.get('task_id')} deleted successfully"
                }
            elif function_name == "update_task":
                return {
                    "success": True,
                    "task_id": function_args.get('task_id'),
                    "message": f"Task {function_args.get('task_id')} updated successfully"
                }
            else:
                return {
                    "success": False,
                    "error": f"Unknown tool: {function_name}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error executing tool {function_name}: {str(e)}"
            }