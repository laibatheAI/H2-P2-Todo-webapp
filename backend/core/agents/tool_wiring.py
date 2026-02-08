"""
Agent-to-tool integration for the Todo AI Chatbot application.
Handles the mapping between agent decisions and MCP tool executions.
"""
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from backend.core.agents.skills import (
    TaskManagementSkill,
    IntentClassificationSkill,
    ConversationContextSkill,
    ConfirmationUXSkill,
    ErrorHandlingSkill
)
from backend.core.agents.todo_agent import TodoAgent
from backend.mcp.tools.task_tools import (
    add_task_tool,
    list_tasks_tool,
    complete_task_tool,
    delete_task_tool,
    update_task_tool
)
from backend.mcp.server import server
from backend.core.agents.intent_classifier import classify_intent, Intent


class ToolMappingResult(BaseModel):
    """
    Result of mapping an agent decision to an appropriate tool.
    """
    success: bool
    tool_name: Optional[str] = None
    tool_parameters: Dict[str, Any] = {}
    message: Optional[str] = None
    error: Optional[str] = None


class AgentToolWiring:
    """
    Class responsible for wiring agent decisions to appropriate MCP tools.
    Maps agent skills to specific tool executions based on classified intent.
    """

    def __init__(self):
        # Initialize skills
        self.task_management_skill = TaskManagementSkill()
        self.intent_classification_skill = IntentClassificationSkill()
        self.conversation_context_skill = ConversationContextSkill()
        self.confirmation_ux_skill = ConfirmationUXSkill()
        self.error_handling_skill = ErrorHandlingSkill()

    def route_to_tool(self, user_input: str, user_id: str) -> ToolMappingResult:
        """
        Route the user input to the appropriate MCP tool based on classified intent.

        Args:
            user_input: The raw input from the user
            user_id: The ID of the authenticated user

        Returns:
            ToolMappingResult indicating which tool to execute and with what parameters
        """
        try:
            # Classify the intent from user input
            classified_intent = classify_intent(user_input)

            # Route to appropriate tool based on intent
            if classified_intent.intent == Intent.ADD_TASK:
                return self._map_add_task(classified_intent, user_id)
            elif classified_intent.intent == Intent.LIST_TASKS:
                return self._map_list_tasks(classified_intent, user_id)
            elif classified_intent.intent == Intent.COMPLETE_TASK:
                return self._map_complete_task(classified_intent, user_id)
            elif classified_intent.intent == Intent.DELETE_TASK:
                return self._map_delete_task(classified_intent, user_id)
            elif classified_intent.intent == Intent.UPDATE_TASK:
                return self._map_update_task(classified_intent, user_id)
            elif classified_intent.intent == Intent.HELP:
                return ToolMappingResult(
                    success=True,
                    tool_name="help",
                    tool_parameters={"message": "help", "user_id": user_id},
                    message="Showing help information"
                )
            else:
                # Unknown intent - return an error or default to help
                return ToolMappingResult(
                    success=False,
                    error=f"Could not understand intent: {classified_intent.intent}. Please try rephrasing your request.",
                    message="I didn't understand your request. Could you rephrase it?"
                )

        except Exception as e:
            return ToolMappingResult(
                success=False,
                error=f"Error routing to tool: {str(e)}",
                message="An error occurred while processing your request"
            )

    def _map_add_task(self, classified_intent: Any, user_id: str) -> ToolMappingResult:
        """
        Map add_task intent to the appropriate tool parameters.

        Args:
            classified_intent: The classified intent object
            user_id: The ID of the authenticated user

        Returns:
            ToolMappingResult for add_task tool
        """
        entities = classified_intent.entities
        original_text = classified_intent.original_text

        # Extract task details from entities and original text
        title = entities.get('title', '')

        # If no title extracted, try to derive it from the original text
        if not title:
            # Simple heuristic to extract task from phrases like "add task to..."
            import re
            match = re.search(r'(?:add|create|make)\s+(?:a\s+)?(?:task|todo|note|item)\s+to\s+(.+?)(?:\.|$)', original_text, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
            else:
                # Just use the original text as the task if nothing else worked
                title = original_text

        # Prepare parameters for the add_task tool
        params = {
            "title": title,
            "description": entities.get('description', ''),
            "priority": entities.get('priority', 'medium'),
            "category": entities.get('category', 'general')
        }

        # Extract date if available
        if 'date' in entities:
            params['due_date'] = entities['date']

        return ToolMappingResult(
            success=True,
            tool_name="add_task",
            tool_parameters=params,
            message=f"Adding task: {title}"
        )

    def _map_list_tasks(self, classified_intent: Any, user_id: str) -> ToolMappingResult:
        """
        Map list_tasks intent to the appropriate tool parameters.

        Args:
            classified_intent: The classified intent object
            user_id: The ID of the authenticated user

        Returns:
            ToolMappingResult for list_tasks tool
        """
        entities = classified_intent.entities

        # Prepare parameters for the list_tasks tool
        params = {
            "status": entities.get('status', 'all'),  # Default to showing all tasks
            "limit": 50,  # Default limit
            "offset": 0   # Default offset
        }

        # Add optional filters if available
        if 'priority' in entities:
            params['priority'] = entities['priority']
        if 'category' in entities:
            params['category'] = entities['category']

        return ToolMappingResult(
            success=True,
            tool_name="list_tasks",
            tool_parameters=params,
            message="Listing tasks"
        )

    def _map_complete_task(self, classified_intent: Any, user_id: str) -> ToolMappingResult:
        """
        Map complete_task intent to the appropriate tool parameters.

        Args:
            classified_intent: The classified intent object
            user_id: The ID of the authenticated user

        Returns:
            ToolMappingResult for complete_task tool
        """
        entities = classified_intent.entities

        # Need to identify which task to complete
        # For now, we'll need to query for a task based on description if no ID provided
        task_id = entities.get('task_id')
        task_title = entities.get('title', '')

        if not task_id and not task_title:
            # If no specific task identified, we might need to list tasks first
            # For now, return an error asking for clarification
            return ToolMappingResult(
                success=False,
                error="Please specify which task to complete. You can say something like 'complete the grocery shopping task'",
                message="Which task would you like to complete?"
            )

        # In a real implementation, we'd need to resolve the task title to an ID
        # For now, we'll simulate with a placeholder ID
        if not task_id and task_title:
            # This would require a lookup in a real system
            task_id = "placeholder-id-for-" + task_title.replace(" ", "-")

        params = {
            "task_id": task_id
        }

        if 'notes' in entities:
            params['completion_notes'] = entities['notes']

        return ToolMappingResult(
            success=True,
            tool_name="complete_task",
            tool_parameters=params,
            message=f"Completing task: {task_id}"
        )

    def _map_delete_task(self, classified_intent: Any, user_id: str) -> ToolMappingResult:
        """
        Map delete_task intent to the appropriate tool parameters.

        Args:
            classified_intent: The classified intent object
            user_id: The ID of the authenticated user

        Returns:
            ToolMappingResult for delete_task tool
        """
        entities = classified_intent.entities

        # Need to identify which task to delete
        task_id = entities.get('task_id')
        task_title = entities.get('title', '')

        if not task_id and not task_title:
            return ToolMappingResult(
                success=False,
                error="Please specify which task to delete. You can say something like 'delete the grocery shopping task'",
                message="Which task would you like to delete?"
            )

        # In a real implementation, we'd need to resolve the task title to an ID
        # For now, we'll simulate with a placeholder ID
        if not task_id and task_title:
            task_id = "placeholder-id-for-" + task_title.replace(" ", "-")

        params = {
            "task_id": task_id
        }

        return ToolMappingResult(
            success=True,
            tool_name="delete_task",
            tool_parameters=params,
            message=f"Deleting task: {task_id}"
        )

    def _map_update_task(self, classified_intent: Any, user_id: str) -> ToolMappingResult:
        """
        Map update_task intent to the appropriate tool parameters.

        Args:
            classified_intent: The classified intent object
            user_id: The ID of the authenticated user

        Returns:
            ToolMappingResult for update_task tool
        """
        entities = classified_intent.entities

        # Need to identify which task to update
        task_id = entities.get('task_id')
        task_title = entities.get('title', '')

        if not task_id and not task_title:
            return ToolMappingResult(
                success=False,
                error="Please specify which task to update. You can say something like 'update the grocery shopping task'",
                message="Which task would you like to update?"
            )

        # In a real implementation, we'd need to resolve the task title to an ID
        # For now, we'll simulate with a placeholder ID
        if not task_id and task_title:
            task_id = "placeholder-id-for-" + task_title.replace(" ", "-")

        # Prepare update parameters
        params = {
            "task_id": task_id
        }

        # Add any specific updates from entities
        if 'title' in entities:
            params['title'] = entities['title']
        if 'description' in entities:
            params['description'] = entities['description']
        if 'date' in entities:
            params['due_date'] = entities['date']
        if 'priority' in entities:
            params['priority'] = entities['priority']
        if 'category' in entities:
            params['category'] = entities['category']
        if 'completed' in entities:
            params['completed'] = entities['completed']

        return ToolMappingResult(
            success=True,
            tool_name="update_task",
            tool_parameters=params,
            message=f"Updating task: {task_id}"
        )

    def execute_mapped_tool(self, tool_mapping_result: ToolMappingResult) -> Dict[str, Any]:
        """
        Execute the tool that was mapped by route_to_tool method.

        Args:
            tool_mapping_result: The result from route_to_tool containing tool name and parameters

        Returns:
            Dictionary with the result of tool execution
        """
        if not tool_mapping_result.success:
            return {
                "success": False,
                "error": tool_mapping_result.error,
                "message": tool_mapping_result.message
            }

        tool_name = tool_mapping_result.tool_name
        tool_params = tool_mapping_result.tool_parameters

        try:
            # Execute the appropriate tool based on the name
            if tool_name == "add_task":
                from pydantic import parse_obj_as
                from backend.mcp.tools.task_tools import AddTaskParams
                params_obj = parse_obj_as(AddTaskParams, tool_params)
                return add_task_tool(params_obj)
            elif tool_name == "list_tasks":
                from pydantic import parse_obj_as
                from backend.mcp.tools.task_tools import ListTasksParams
                params_obj = parse_obj_as(ListTasksParams, tool_params)
                return list_tasks_tool(params_obj)
            elif tool_name == "complete_task":
                from pydantic import parse_obj_as
                from backend.mcp.tools.task_tools import CompleteTaskParams
                params_obj = parse_obj_as(CompleteTaskParams, tool_params)
                return complete_task_tool(params_obj)
            elif tool_name == "delete_task":
                from pydantic import parse_obj_as
                from backend.mcp.tools.task_tools import DeleteTaskParams
                params_obj = parse_obj_as(DeleteTaskParams, tool_params)
                return delete_task_tool(params_obj)
            elif tool_name == "update_task":
                from pydantic import parse_obj_as
                from backend.mcp.tools.task_tools import UpdateTaskParams
                params_obj = parse_obj_as(UpdateTaskParams, tool_params)
                return update_task_tool(params_obj)
            elif tool_name == "help":
                return {
                    "success": True,
                    "message": "I'm your Todo AI Assistant. I can help you manage your tasks. You can ask me to add, list, update, complete, or delete tasks.",
                    "supported_actions": ["add task", "list tasks", "update task", "complete task", "delete task"]
                }
            else:
                return {
                    "success": False,
                    "error": f"Unknown tool: {tool_name}",
                    "message": "An error occurred while processing your request"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error executing tool {tool_name}: {str(e)}",
                "message": "An error occurred while executing the requested action"
            }


# Global instance for tool wiring
agent_tool_wiring = AgentToolWiring()


def route_and_execute_tool(user_input: str, user_id: str) -> Dict[str, Any]:
    """
    Convenience function to route user input to appropriate tool and execute it.

    Args:
        user_input: The raw input from the user
        user_id: The ID of the authenticated user

    Returns:
        Dictionary with the result of tool execution
    """
    mapping_result = agent_tool_wiring.route_to_tool(user_input, user_id)
    return agent_tool_wiring.execute_mapped_tool(mapping_result)